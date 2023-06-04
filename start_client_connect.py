#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from os.path import exists
import subprocess
import pprint
import bson
import os


# Global variables
clients_list = []
ec = 0
dbs = []


def generate_py(col, con, db, path):
	f = open("py_template.py", 'r')
	w = open(f"py/{db}_{col}.py", 'w')
	w.write(f"col = '{col}'\n")
	w.write(f"con = '{con}'\n")
	w.write(f"db = '{db}'\n")
	w.write(f"path = '{path}'\n")

	for line in f:
		w.write(line)

	w.close()
	f.close()
	return f"py/{db}_{col}.py"


def generate_py_actuate(rcon, scol, scon, db, path):
	f = open("py_template_0.py", 'r')
	w = open(f"py/{db}_{scol}_actuate.py", 'w')
	w.write(f"col = '{scol}'\n")
	w.write(f"rcon = '{rcon}'\n")
	w.write(f"con = '{scon}'\n")
	w.write(f"db = '{db}'\n")
	w.write(f"path = '{path}'\n")

	for line in f:
		w.write(line)

	w.close()
	f.close()
	return f"py/{db}_{scol}_actuate.py"


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
	arg = "[" + str(len(collections)) + "] All collections" 
	print(arg)
	print("\nSelect a collection to connect to Central Point:")
	sel = input("Enter: ")
	if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(collections):
			print("Invalid input!\n")
			view_collection()
	elif int(sel) == len(collections):
		if clients_list[ec][2] == "sensor":
			print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
			for col in collections:
				path = f"py/dump/{database_name}/{col}/"
				pyfile = generate_py(col, con, database_name, path)
				command = f"gnome-terminal --tab --title={database_name}/{col} -- bash -c 'python3 {pyfile} ;bash'"
				dep = subprocess.run(command, shell=True, capture_output=True)
		elif clients_list[ec][2] == "actuator":
			print_clients()
			print("[n] None (store actuation data in Central Point only)")
			print("\n\nSelect recipient of actuation data")
			s = input("Enter:")
			if s.isdigit() == 0 or int(s) < -1 or int(s) > len(clients_list)-1:
				if s == 'n' or s == 'N':
					print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
					for col in collections:
						path = f"py/dump/{database_name}/{col}_actuate/"
						pyfile = generate_py_actuate(main_connection_string, col, con, database_name, path)
						command = f"gnome-terminal --tab --title={database_name}/{col}_actuate -- bash -c 'python3 {pyfile} ;bash'"
						dep = subprocess.run(command, shell=True, capture_output=True)
				print("Invalid input!\n")
				view_collection(con, database_name, dev_id)
			else:
				print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
				for col in collections:
					rcon = clients_list[int(s)][3]
					path = f"py/dump/{database_name}/{col}_actuate/"
					pyfile = generate_py_actuate(rcon, col, con, database_name, path)
					command = f"gnome-terminal --tab --title={database_name}/{col}_actuate -- bash -c 'python3 {pyfile} ;bash'"
					dep = subprocess.run(command, shell=True, capture_output=True)

	else:
		if clients_list[ec][2] == "sensor":
			collection_name = collections[int(sel)]
			print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
			path = f"py/dump/{database_name}/{collection_name}/"
			pyfile = generate_py(collection_name, con, database_name, path)
			command = f"gnome-terminal --tab --title={database_name}/{collection_name} -- bash -c 'python3 {pyfile} ;bash'"
			dep = subprocess.run(command, shell=True, capture_output=True)
		elif clients_list[ec][2] == "actuator":
			print_clients()
			print("[n] None (store actuation data in Central Point only)")
			print("\n\nSelect recipient of actuation data")
			s = input("Enter:")
			if s.isdigit() == 0 or int(s) < -1 or int(s) > len(clients_list)-1:
				if s == 'n' or s == 'N':
					collection_name = collections[int(sel)]
					print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
					path = f"py/dump/{database_name}/{collection_name}_actuate/"
					pyfile = generate_py_actuate(main_connection_string, collection_name, con, database_name, path)
					command = f"gnome-terminal --tab --title={database_name}/{collection_name}_actuate -- bash -c 'python3 {pyfile} ;bash'"
					dep = subprocess.run(command, shell=True, capture_output=True)
				print("Invalid input!\n")
				view_collection(con, database_name, dev_id)
				
			else:
				rcon = clients_list[int(s)][3]
				collection_name = collections[int(sel)]
				print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
				path = f"py/dump/{database_name}/{collection_name}_actuate/"
				pyfile = generate_py_actuate(rcon, collection_name, con, database_name, path)
				command = f"gnome-terminal --tab --title={database_name}/{collection_name}_actuate -- bash -c 'python3 {pyfile} ;bash'"
				dep = subprocess.run(command, shell=True, capture_output=True)

	select_client()
		

def start_connect():
	global dbs
    
	if clients_list[ec][0] == 1:
		collection = main_db.mqtt_clients
	elif clients_list[ec][0] == 2:
		collection = main_db.http_clients
	elif clients_list[ec][0] == 3:
		# Connect to client
		collection = main_db.mongodb_clients
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
		# Check existence in central point
		dbnames = main_client.list_database_names()
		if dbnamae in dbnames:
			print("\nDatabase '", dbnamae, "' already exists. Remove existing collections in this database to avoid dangling objects? (y/n)", sep='')
			sel = input("Enter: ")
			if sel != 'n' and sel != 'N':
				print("\nDropping collections...\n\n")
				command = f"main_client.{dbnamae}"
				DB = eval(command)
				for col in DB.list_collection_names():
					command = f"DB.{col}.drop()"
					eval(command)
			else:
				print("\nProceeding.")
		view_collection(con, dbnamae, dev_id)


def print_clients():
    print('')
    collection1 = main_db.mqtt_clients
    collection2 = main_db.http_clients
    collection3 = main_db.mongodb_clients

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
        post = '[' + str(ctr) + ']' + " - [" + doc["type"] + '] ' + doc["care1_device_id"] + '-' + doc["URI"]
        print(post)
        clients_list.append([3, doc["_id"], doc["type"], doc["URI"]])
        ctr = ctr + 1
    print('')


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


print("START CLIENT CONNECTION")
# MongoDB configuration
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())
main_password = os.environ.get("MONGODB_PW")
main_connection_string = f"mongodb+srv://care1:{main_password}@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority"
main_client = MongoClient(main_connection_string)
main_db = main_client.CARE1

'''
# Drop previous connection data
db1 = main_client.mongodb_client_readings
for col in db1.list_collection_names():
	if col == "do_not_delete":
		continue
	command = f"db1.{col}.drop()"
	eval(command)
'''

select_client()