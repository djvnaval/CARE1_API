col = 'solenoidValve_actuate'
rcon = 'mongodb+srv://care1:care1project@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority'
con = 'mongodb+srv://jan11backupstorage:47PIN8N6QdVK2afx@actuatoripe.woncb4j.mongodb.net/'
db = 'oneM2M_HTTP_SmartFarm'
path = 'data/dump/oneM2M_HTTP_SmartFarm/solenoidValve_actuate/'


from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from os.path import exists
import subprocess
import datetime
import pprint
import bson
import time
import os


# This part is for debugging purposes only
recorder = f"data/log/{db}_{col}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.txt"


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
                        #doc.update({"_id": time_int(datetime.datetime.now())})
                        db[coll.split('.')[0]].insert_one(doc)
                        d = datetime.datetime.now()
                        write = d.strftime('%Y-%m-%d_%H_%M %S.%f') + '\n'
                        r.write(write)
                        print(doc)

print("START CLIENT CONNECTION")
print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
rec = open(recorder, 'w')
rec.close()
while 1:
    rec = open(recorder, 'a')

    '''
    dump([col], con, db, path)
    restore(path, rcon, db)
    '''

    # Source
    client = MongoClient(con)
    command = f"client.{db}.{col}"
    coll = eval(command)
    results = coll.find().sort("time", -1).limit(10)

    # Destination
    client1 = MongoClient(rcon)
    command = f"client1.{db}"
    db1 = eval(command)

    for r in results:
        if db1[col].count_documents(r) == 0:
            db1[col].insert_one(r)
            d = datetime.datetime.now()
            write = d.strftime('%Y-%m-%d_%H_%M %S.%f') + '\n'
            rec.write(write)
            print(r)

    print("Connection is ongoing...")
    rec.close()