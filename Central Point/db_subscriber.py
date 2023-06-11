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

MQTT_USERNAME = "<change-mqtt-username>"
MQTT_PASSWORD = "<change-mqtt-password>"
HOST = 'change-mqtt-host'
PORT = 8883

MONGO_URI = 'change-mongodb-uri'

prev_rqi = ''

def on_connect(client, userdata, flags, rc):
    print('CONNACK received with code %d.' % (rc))

    client.subscribe('#', qos=1)

def on_message(client, userdata, message):
    payload = json.loads(message.payload)

    global prev_rqi

    # In OpenMTC,
    # topic = onem2m/MQTT_<system:SmartFarm/AQM>/<sensor>
    topic = payload['to'].split('/')
    
    if topic[1] != None:
        if topic[1] == "MQTT_SmartFarm":
            db = smartfarm_db
            db_name = "oneM2M_MQTT_SmartFarm"
        elif topic[1] == "MQTT_AQM":
            db = aqm_db
            db_name = "oneM2M_MQTT_AQM"

    rqi = payload['rqi']

    try:
        pc = payload['pc']
        cin = pc['m2m:cin']
        con = cin['con']

        decodedBytes = base64.b64decode(con)
        decodedStr = decodedBytes.decode("utf-8")
        con_str = json.loads(decodedStr)

        if topic[2] != None and topic[2] not in db.list_collection_names():
            pymongo.collection.Collection(db, topic[2], create=True)
            print("Created collection with name:", topic[2], "in database", db_name,  "\n")
        
        if rqi != prev_rqi:
            col = pymongo.collection.Collection(db, topic[2], create=False)
            col.insert_one(con_str)
            print("Inserted ", con_str, " to Collection", topic[2], "in database", db_name, "\n")
            prev_rqi = rqi
    except:
        pass



# Setup MQTT broker connection
client = mqtt.Client(client_id='mongodb-subscriber')
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(HOST, PORT)

# Setup MongoDB connection
mongo_client = pymongo.MongoClient(MONGO_URI)

smartfarm_db = mongo_client.oneM2M_MQTT_SmartFarm
aqm_db = mongo_client.oneM2M_MQTT_AQM

# Start to listen to the HiveMQ Broker
client.loop_forever()