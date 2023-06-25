col = 'solenoidValve_actuate'
rcon = 'mongodb+srv://HTTPSystem:HTTPnonOneM2M@nononem2m.lold0yl.mongodb.net/?retryWrites=true&w=majority'
con = 'mongodb+srv://care1:care1project@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority'
db = 'HTTPSmartFarm'
path = 'data/dump/HTTPSmartFarm/solenoidValve_actuate_actuate/'


from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from os.path import exists
import subprocess
import datetime
import pprint
import bson
import time
import os


def time_int(d): # d=datetime.datetime.now()
    time.sleep(1)
    return int(d.strftime("%Y%m%d%H%M%S"))


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
                        #doc.update({"_id": time_int(datetime.datetime.now())})
                        db[coll.split('.')[0]].insert_one(doc)
                        print(doc)

print("START CLIENT CONNECTION")
print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
while 1:
    dump([col], con, db, path)
    restore(path, rcon, db)
    print("Connection is ongoing...")