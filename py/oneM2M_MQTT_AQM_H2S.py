col = 'H2S'
con = 'mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority'
db = 'oneM2M_MQTT_AQM'
path = 'py/dump/oneM2M_MQTT_AQM/H2S/'
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from os.path import exists
import subprocess
import pprint
import bson
import os


def dump(collections, conn, db_name, path):
    client = MongoClient(conn)
    command = f"client.{db_name}"
    db = eval(command)
    if not os.path.exists(path):
    	os.makedirs(path)
    for coll in collections:
        with open(os.path.join(path, f'{coll}.bson'), 'wb+') as f:
            for doc in db[coll].find():
                f.write(bson.BSON.encode(doc))


def restore(path, conn, db_name):
    client = MongoClient(conn)
    command = f"client.{db_name}"
    db = eval(command)
    for coll in os.listdir(path):
        if coll.endswith('.bson'):
            with open(os.path.join(path, coll), 'rb+') as f:
            	for doc in bson.decode_all(f.read()):
            		if db[coll.split('.')[0]].count_documents(doc) == 0:
            			db[coll.split('.')[0]].insert_one(doc)
            			print(doc)

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

print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
while 1:
    dump([col], con, db, path)
    restore(path, main_connection_string, db)
    print("Connection is ongoing...")