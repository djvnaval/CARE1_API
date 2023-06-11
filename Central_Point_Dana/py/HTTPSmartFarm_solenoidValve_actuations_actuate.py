col = 'solenoidValve_actuations'
rcon = 'mongodb+srv://HTTPSystem:HTTPnonOneM2M@nononem2m.lold0yl.mongodb.net/?retryWrites=true&w=majority'
con = 'mongodb+srv://jan11backupstorage:47PIN8N6QdVK2afx@actuatoripe.woncb4j.mongodb.net/'
db = 'HTTPSmartFarm'
path = 'py/dump/HTTPSmartFarm/solenoidValve_actuations_actuate/'


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
        with open(os.path.join(path, f'{coll}_actuate.bson'), 'wb+') as f:
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
print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
while 1:
    dump([col], con, db, path)
    restore(path, rcon, f"{db}_actuate")
    print("Connection is ongoing...")