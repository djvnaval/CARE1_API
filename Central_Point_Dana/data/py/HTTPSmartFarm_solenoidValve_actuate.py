col = 'solenoidValve_actuate'
rcon = 'mongodb+srv://HTTPSystem:HTTPnonOneM2M@nononem2m.lold0yl.mongodb.net/?retryWrites=true&w=majority'
con = 'mongodb+srv://care1:care1project@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority'
db = 'HTTPSmartFarm'
path = 'data/dump/HTTPSmartFarm/solenoidValve_actuate/'


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

print("START CLIENT CONNECTION")
print("\nCONNECTION IS ESTABLISHED SUCCESSFULLY!\n")
rec = open(recorder, 'w')
rec.close()
while 1:
    rec = open(recorder, 'a')
    di = datetime.datetime.now()

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
            if float(d.strftime('%S.%f')) - float(di.strftime('%S.%f')) >= 0:
                write = str(float(d.strftime('%S.%f')) - float(di.strftime('%S.%f'))) + '\n'
                rec.write(write)
            print(r)

    print("Connection is ongoing...")
    rec.close()