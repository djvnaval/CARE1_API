#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


import subprocess
from os.path import exists
import os
import pprint
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv


# Global variables
clients_list = []
ec = 0
dbs = []
MAIN_CON_STRING = ""


def show_collection(cl):
	cursor = cl.find()
	print(cl)
	for doc in cursor:
		for item in doc:
			print(doc[item])
	start()


def view_collection(con, database_name, dev_id):
	client = MongoClient(con)
	command = f"client.{database_name}.list_collection_names()"
	collections = []
	ctr = 0
	for col in eval(command):
		arg = '[' + str(ctr) + "] " + col
		print(arg)
		collections.append(col)
		ctr = ctr + 1
	print("\nSelect a collection to connect to Central Point:")
	sel = input("Enter: ")
	if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(collections)-1:
			print("Invalid input!\n")
			view_collection()
	collection_name = collections[int(sel)]
	command = f"client.{database_name}.{collection_name}"
	coll = eval(command)
	main_client = MongoClient(MAIN_CON_STRING)
	main_db = main_client.mongodb_client_readings
	command = f"main_db.{dev_id}"
	main_col = eval(command)
	for doc in coll.find():
		main_col.insert_one(doc)
		print("Device readings transferred to Central Point's database!")


def start_connect():
	global dbs
	global MAIN_CON_STRING
	load_dotenv(find_dotenv())
	password = os.environ.get("MONGODB_PW")
	connection_string = f"mongodb+srv://care1:{password}@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority"
	MAIN_CON_STRING = connection_string
	client = MongoClient(connection_string)
	db = client.CARE1
    
	if clients_list[ec][0] == 1:
		collection = db.mqtt_clients
	elif clients_list[ec][0] == 2:
		collection = db.http_clients
	elif clients_list[ec][0] == 3:
		# Connect to client
		collection = db.mongodb_clients
		clii = collection.find({"_id" : clients_list[ec][1]})
		for doc in clii:
			con = doc["URI"]
			dev_id = doc["care1_device_id"]
		cli = MongoClient(con)
		print("\nAVAILABLE DATABASES")
		ctr = 0
		for dbname in enumerate(cli.list_databases()):
			arg = '[' + str(ctr) + '] ' + str(dbname[1]['name'])
			print(arg)
			dbs.append(str(dbname[1]['name']))
			ctr = ctr + 1
		sel = input("\nSelect a database to view: ")
		if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > ctr-1:
			print("Invalid input!\n")
			start_connect()
		dbnamae = dbs[int(sel)]
		view_collection(con, dbnamae, dev_id)


def select_client():
    global ec
    print_clients()
    print("SELECT A CLIENT TO START")
    sel = input("Enter: ") # Selection
    print('')
    if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(clients_list)-1:
        print("Invalid input!\n")
        select_client()
    ec = int(sel)
    start_connect()


def print_clients():
    print('')
    # MongoDB configuration
    from dotenv import load_dotenv, find_dotenv
    import os
    import pprint
    from pymongo import MongoClient
    load_dotenv(find_dotenv())
    password = os.environ.get("MONGODB_PW")
    connection_string = f"mongodb+srv://care1:{password}@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client.CARE1
    collection1 = db.mqtt_clients
    collection2 = db.http_clients
    collection3 = db.mongodb_clients

    global clients_list
    clients_list.clear()

    print("EXISTING CLIENTS:")
    ctr = 0
    for doc in collection1.find():
        post = '[' + str(ctr) + ']' + ' - [' + doc["type"] + "_MQTT" + '] ' + doc["care1_device_id"] + '-' + doc["broker"] + ':' + doc["port"]
        print(post)
        post = "      Topics: " + str(doc["topics"])
        print(post)
        clients_list.append([1, doc["_id"]])
        ctr = ctr + 1
    for doc in collection2.find():
        post = '[' + str(ctr) + ']' + ' - [' + doc["type"] + "_HTTP" + '] ' + doc["care1_device_id"] + '-' + doc["broker"] + ':' + doc["port"]
        print(post)
        post = "      Topics: " + str(doc["topics"])
        print(post)
        clients_list.append([2, doc["_id"]])
        ctr = ctr + 1
    for doc in collection3.find():
        post = '[' + str(ctr) + ']' + " - [PUB_" + doc["protocol"] + '] ' + doc["care1_device_id"] + '-' + doc["URI"]
        print(post)
        clients_list.append([3, doc["_id"]])
        ctr = ctr + 1
    print('')


def start():
	print("START CLIENT CONNECTION")
	select_client()

start()