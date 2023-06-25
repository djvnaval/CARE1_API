# prototype of central point's Actuator_IPE.py


from pymongo import MongoClient
import time
import datetime
import random


# MongoDB configuration
uri = 'mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority'
main_client = MongoClient(uri)


def actuate(db, col, t, limit):
	if limit == 0:
		print("endless")
	else:
		#command = f"main_client.{db}.{col}.insert_one(post)"
		for i in range(limit):
			time.sleep(t)
			val = random.randint(0,1)
			post = {
				"value" : val,
				"type" : "solenoid valve",
				"unit" : "none",
				"time" : datetime.datetime.now()
			}
			#eval(command)
			main_client.oneM2M_MQTT_SmartFarm.solenoidValve.insert_one(post)
			print(post)


actuate("oneM2M_MQTT_SmartFarm", "solenoidValve", 10, 100)