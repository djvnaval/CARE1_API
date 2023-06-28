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


def generate_py(col, con, db, path): # Sensors
	f = open("py_template.py", 'r')
	w = open(f"data/py/{db}_{col}.py", 'w')
	w.write(f"col = '{col}'\n")
	w.write(f"con = '{con}'\n")
	w.write(f"db = '{db}'\n")
	w.write(f"path = '{path}'\n")

	for line in f:
		w.write(line)

	w.close()
	f.close()
	return f"data/py/{db}_{col}.py"


def generate_py_actuate(rcon, scol, scon, db, path): # Actuation switches
	f = open("py_template_0.py", 'r')
	w = open(f"data/py/{db}_{scol}.py", 'w')
	w.write(f"col = '{scol}'\n")
	w.write(f"rcon = '{rcon}'\n")
	w.write(f"con = '{scon}'\n")
	w.write(f"db = '{db}'\n")
	w.write(f"path = '{path}'\n")

	for line in f:
		w.write(line)

	w.close()
	f.close()
	return f"data/py/{db}_{scol}.py"


def view_collection(con, database_name, dev_id):
	print("\n\nCOLLECTIONS IN", database_name)
	client = MongoClient(con)
	command = f"client.{database_name}.list_collection_names()"
	collections = []
	ctr = 0

	if clients_list[ec][2] == "sensor":
		# central point database check
		dbnames = main_client.list_database_names()
		if database_name in dbnames:
			print("\n\nDatabase '", database_name, "' already exists. Sync existing collections in this database to avoid dangling objects? (y/n)", sep='')
			sel = input("Enter: ")
			if sel != 'n' and sel != 'N':
				print("\nSyncing collections...")
				x = f"main_client.{database_name}"
				DB = eval(x)
				for col in DB.list_collection_names():
					x = f"DB.{col}.drop()"
					eval(x)
			else:
				print("\n\nProceeding.")

		for col in eval(command):
			arg = '[' + str(ctr) + "] " + col
			print(arg)
			collections.append(col)
			ctr = ctr + 1
		arg = "[" + str(len(collections)) + "] All collections" 
		print(arg)
		print("\n\nSelect collection/s to connect to Central Point")
		sel = input("\nEnter: ")

		if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(collections):
				print("\n\nInvalid input!")
				view_collection(con, database_name, dev_id)
		elif int(sel) == len(collections):
			print("\n\nCONNECTION IS ESTABLISHED SUCCESSFULLY!")
			for col in collections:
				path = f"data/dump/{database_name}/{col}/"
				pyfile = generate_py(col, con, database_name, path)
				y = f"gnome-terminal --tab --title={database_name}/{col} -- bash -c 'python3 {pyfile} ;bash'"
				dep = subprocess.run(y, shell=True, capture_output=True)
		else:
			collection_name = collections[int(sel)]
			print("\n\nCONNECTION IS ESTABLISHED SUCCESSFULLY!")
			path = f"data/dump/{database_name}/{collection_name}/"
			pyfile = generate_py(collection_name, con, database_name, path)
			u = f"gnome-terminal --tab --title={database_name}/{collection_name} -- bash -c 'python3 {pyfile} ;bash'"
			dep = subprocess.run(u, shell=True, capture_output=True)

	elif clients_list[ec][2] == "actuation switch":
		for col in eval(command):
			arg = '[' + str(ctr) + "] " + col
			print(arg)
			collections.append(col)
			ctr = ctr + 1
		print("\n\nSelect collection containing actuations to be sent")
		sel = input("\nEnter: ")

		if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(collections) - 1:
				print("\n\nInvalid input!")
				view_collection(con, database_name, dev_id)
		else:
			print_clients()
			print("[n] None (store actuation data in Central Point only)")
			print("\n\nSelect recipient of actuation data")
			s = input("\nEnter: ")
			if s.isdigit() == 0 or int(s) < -1 or int(s) > len(clients_list) - 1:
				if s == 'n' or s == 'N':
					# central point database check
					dbnames = main_client.list_database_names()
					if database_name in dbnames:
						print("\nSyncing collections...")
						p = f"main_client.{database_name}"
						DB = eval(p)
						for ccc in DB.list_collection_names():
							if ccc == collections[int(sel)]:
								print(f"\n\n{ccc} already exists in the recipent database. Sync to avoid dangling objects? (y/n)")
								act = input("Enter: ")
								if act != 'n' and act != 'N':
									k = f"DB.{ccc}.drop()"
									eval(k)
								break

					collection_name = collections[int(sel)]
					print("\n\nCONNECTION IS ESTABLISHED SUCCESSFULLY!")
					path = f"data/dump/{database_name}/{collection_name}/"
					pyfile = generate_py_actuate(main_connection_string, collection_name, con, database_name, path)
					ll = f"gnome-terminal --tab --title={database_name}/{collection_name} -- bash -c 'python3 {pyfile} ;bash'"
					dep = subprocess.run(ll, shell=True, capture_output=True)
				else:
					print("\n\nInvalid input!")
					view_collection(con, database_name, dev_id)
			else:
				# recipient database check
				client__ = MongoClient(clients_list[int(s)][3])
				dbnames = client__.list_database_names()
				if database_name in dbnames:
					print("\nSyncing collections...")
					mm = f"client__.{database_name}"
					DB = eval(mm)
					for ccc in DB.list_collection_names():
						if ccc == collections[int(sel)]:
							print(f"\n\n{ccc} already exists in the recipent database. Sync to avoid dangling objects? (y/n)")
							act = input("Enter: ")
							if act != 'n' and act != 'N':
								qq = f"DB.{ccc}.drop()"
								eval(qq)
							break

					else:
						print("\n\nProceeding.")

				collection_name = collections[int(sel)]
				print("\n\nCONNECTION IS ESTABLISHED SUCCESSFULLY!")
				path = f"data/dump/{database_name}/{collection_name}/"
				pyfile = generate_py_actuate(clients_list[int(s)][3], collection_name, con, database_name, path)
				aa = f"gnome-terminal --tab --title={database_name}/{collection_name} -- bash -c 'python3 {pyfile} ;bash'"
				dep = subprocess.run(aa, shell=True, capture_output=True)
	else:
		print("\n\nIf client device selected is a subscriber, select a publisher to connect to it first.")

	select_client()
		

def start_connect():
	print("START CLIENT CONNECTION")
	global dbs

	if clients_list[ec][0] == 0:

		# Connect to client
		collection = main_db.mongodb_clients
		clii = collection.find({"_id" : clients_list[ec][1]})
		for doc in clii:
			con = doc["URI"]
			dev_id = doc["care1_device_id"]
		cli = MongoClient(con)
		print("\n\nAVAILABLE DATABASES")

		ctr = 0
		for dbname in enumerate(cli.list_databases()):
			arg = '[' + str(ctr) + '] ' + str(dbname[1]['name'])
			print(arg)
			dbs.append(str(dbname[1]['name']))
			ctr = ctr + 1
		sel = input("\nSelect a database to view: ")

		if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > ctr-1:
			print("\n\nInvalid input!")
			start_connect()
		dbnamae = dbs[int(sel)]

		view_collection(con, dbnamae, dev_id)


def print_clients():
    collection = main_db.mongodb_clients
    global clients_list
    clients_list.clear()

    print("\n\nEXISTING CLIENTS:")
    ctr = 0
    for doc in collection.find():
        post = '[' + str(ctr) + ']' + " - [" + doc["type"] + '] ' + doc["device"] + " : " + doc["care1_device_id"] + " : " + doc["protocol"]
        print(post)
        clients_list.append([0, doc["_id"], doc["device"], doc["URI"]])
        ctr = ctr + 1


def select_client():
    global ec
    print_clients()
    print("\n\nSELECT A CLIENT TO START")
    sel = input("\nEnter: ") # Selection
    print('')
    if sel.isdigit() == 0 or int(sel) < -1 or int(sel) > len(clients_list)-1:
        print("\n\nInvalid input!")
        select_client()
    ec = int(sel)
    start_connect()


# START


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


select_client()