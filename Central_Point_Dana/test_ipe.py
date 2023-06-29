#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


from bson.objectid import ObjectId
from pymongo import MongoClient
import time
import datetime
import random


# MongoDB configuration
main_connection_string = "mongodb+srv://jan11backupstorage:47PIN8N6QdVK2afx@actuatoripe.woncb4j.mongodb.net/"
main_client = MongoClient(main_connection_string)


def actuate(db, col, t, limit):
	# central point database check
	dbnames = main_client.list_database_names()
	if db in dbnames:
		print("\n\nCleaning actuation database...")
		command = f"main_client.{db}"
		DB = eval(command)
		for cc in DB.list_collection_names():
			command = f"DB.{cc}.drop()"
			eval(command)

	command = f"main_client.{db}.{col}_actuate.insert_one(post)"
	for i in range(limit):
		time.sleep(t)
		val = random.randint(0,1)
		post = {
			"value" : val,
			"type" : "solenoid valve",
			"unit" : "none",
			"time" : datetime.datetime.now()
		}
		eval(command)
		print(post)


#actuate("HTTPSmartFarm", "solenoidValve", 2, 1)
actuate("HTTPSmartFarm", "solenoidValve", 2, 300)
#actuate("oneM2M_MQTT_SmartFarm", "solenoidValve", 5, 100)