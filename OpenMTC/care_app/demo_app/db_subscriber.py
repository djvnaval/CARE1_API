#######################################################################
#
# This connects the MongoDB Atlas as a subscriber to HiveMQ Broker
#
# Note: This stands as the integration between the HiveMQ Cloud and
#       MongoDB database while the feature is still under construction
#
# Created on June 1, 2023
# @author: Mariel V. Tatel
#
#######################################################################

import paho.mqtt.client as mqtt
import json
import pymongo
import ssl
import base64

from datetime import datetime

MQTT_USERNAME = "mongoDB"
MQTT_PASSWORD = "mongoDBcare1"
MQTT_HOST = '29c49bdf585f4e6d8e93e1522dc5e23f.s1.eu.hivemq.cloud'
MQTT_PORT = 8883

MONGO_URI = 'mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority'

prev_rqi = ''

def on_connect(client, userdata, flags, rc):
    print('CONNACK received with code %d.' % (rc))

    client.subscribe('#', qos=1)

def on_message(client, userdata, message):
    payload = json.loads(message.payload)

    global prev_rqi

    # topic = onem2m/MQTT_<system:SmartFarm/AQM>/devices_mqtt/<sensor>
    topic = payload['to'].split('/')
    
    try:
        if topic[1] != None:
            if topic[1] == "MQTT_SmartFarm":
                db = smartfarm_db
                db_name = "oneM2M_MQTT_SmartFarm"
            elif topic[1] == "MQTT_AQM":
                db = aqm_db
                db_name = "oneM2M_MQTT_AQM"
    except:
        pass

    rqi = payload['rqi']

    try:
        topic_name = topic[2]

        if topic_name == 'measurements':
            topic_name = topic[3]
    except:
        pass

    try:
        pc = payload['pc']
        cin = pc['m2m:cin']
        con = cin['con']

        decodedBytes = base64.b64decode(con)
        decodedStr = decodedBytes.decode("utf-8")
        con_str = json.loads(decodedStr)

        con_str['time'] = datetime.strptime(con_str['time'], '%Y-%m-%d %H:%M:%S.%f')

        if topic_name != None and topic_name not in db.list_collection_names():
            pymongo.collection.Collection(db, topic_name, create=True)
            print("Created collection with name:", topic_name, "in database", db_name,  "\n")
        
        if rqi != prev_rqi:
            col = pymongo.collection.Collection(db, topic_name, create=False)
            col.insert_one(con_str)
            print("Inserted ", con_str, " to Collection", topic_name, "in database", db_name, "\n")
            prev_rqi = rqi
    except:
        pass


# Setup MQTT broker connection
client = mqtt.Client(client_id='mongodb-subscriber')
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_HOST, MQTT_PORT)

# Setup MongoDB connection
mongo_client = pymongo.MongoClient(MONGO_URI)

smartfarm_db = mongo_client.oneM2M_MQTT_SmartFarm
aqm_db = mongo_client.oneM2M_MQTT_AQM

# Start to listen to the HiveMQ Broker
client.loop_forever()