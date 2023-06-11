#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


from pymongo import MongoClient
import time
import datetime
import random


# MongoDB configuration
main_connection_string = "mongodb+srv://jan11backupstorage:47PIN8N6QdVK2afx@actuatoripe.woncb4j.mongodb.net/"
main_client = MongoClient(main_connection_string)


def actuate(db, col, t, limit):
	if limit == 0:
		print("endless")
	else:
		command = f"main_client.{db}.{col}.insert_one(post)"
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

#actuate("HTTPSmartFarm", "solenoidValve", 10, 100)
actuate("oneM2M_HTTP_SmartFarm", "solenoidValve", 10, 100)
actuate("oneM2M_MQTT_SmartFarm", "solenoidValve", 10, 100)