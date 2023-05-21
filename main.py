#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


import subprocess
from os.path import exists


# Global variables
clients = "src/clients.txt"
terms = "src/TERMS_AND_CONDITIONS.txt"
MQTTp = "src/MQTTp_note.txt"
MQTTs = "src/MQTTs_note.txt"
MDBp = "src/MongoDBp_note.txt"
clients_list = []

# edit_client() variables
ec = 0
data = []
ed = 0


def edit_client_1(eid):
    global ec
    global data
    global ed

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
    
    if clients_list[ec][0] == 1:
        collection = db.mqtt_clients
        # This section is specifically inclined to MQTT client_adder
        if ed == 5:
            arg = str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            print("Select NEW type:\n[0] PUB (publishing client)\n[1] SUB (subscribing client)")
            action = input("\nEnter: ")
            if action == '0':
                data[ed][1] = "PUB"
                print("\nClient attribute edited successfully.")
            elif action == '1':
                data[ed][1] = "SUB"
                print("\nClient attribute edited successfully.")
            else:
                print("Invalid input! Type is not changed.\n")
        elif ed == 6:
            print(data[ed])
            print("Topics and QOS:")
            for item in data[ed][1]:
                s = item[0] + " : " + str(item[1])
                print(s)
            topic_str = []
            qos = []
            n_topics = 0
            n_topics = int(input("Number of topics (if leaving blank and editing later, type '0'): "))
            if n_topics != 0:
                for i in range(n_topics):
                    arg = "Topic String " + str(i+1) + ": "
                    topic_str.append(input(arg))
                    qos.append(int(input("Quality of Service (QOS): ")))
            else:
                print("Topics are to be added later.")

            topics = []
            for i in range(n_topics):
                topics.append([topic_str[i], qos[i]])
            data[ed][1] = topics
            print("\nClient attribute edited successfully.")
        else:
            arg = str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            arg = "Enter NEW " + str(data[ed][0]) + ": "
            new = input(arg)
            if new != '\n' or new != '':
                data[ed][1] = new.strip('\n')
                print("\nClient attribute edited successfully.")

        # Modifying in MongoDB
        post = {
            "care1_device_id" : data[0][1],
            "broker" : data[1][1],
            "port" : data[2][1],
            "username" : data[3][1],
            "password" : data[4][1],
            "type" : data[5][1],
            "topics" : data[6][1]
        }

        # Removing old document in MongoDB
        collection.delete_one({"_id" : eid})

        post_id = collection.insert_one(post).inserted_id
        response = "\nClient successfully modified with id " + str(post_id) + "."
        print(response)

    elif clients_list[ec][0] == 2:
        collection = db.http_clients

    elif clients_list[ec][0] == 3:
        collection = db.mongodb_clients
        # This section is specifically inclined to MongoDB client_adder
        if ed == 2:
            arg = str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            print("Select NEW protocol:\n[0] HTTP\n[1] MQTT")
            action = input("\nEnter: ")
            if action == '0':
                data[ed][1] = "HTTP"
                print("\nClient attribute edited successfully.")
            elif action == '1':
                data[ed][1] = "MQTT"
                print("\nClient attribute edited successfully.")
            else:
                print("Invalid input! Type is not changed.\n")
        else:
            arg = str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            arg = "Enter NEW " + str(data[ed][0]) + ": "
            new = input(arg)
            if new != '\n' or new != '':
                data[ed][1] = new.strip('\n')
                print("\nClient attribute edited successfully.")

        # Modifying in MongoDB
        post = {
            "care1_device_id" : data[0][1],
            "URI" : data[1][1],
            "protocol" : data[2][1],
        }

        # Removing old document in MongoDB
        collection.delete_one({"_id" : eid})

        post_id = collection.insert_one(post).inserted_id
        response = "\nClient successfully modified with id " + str(post_id) + "."
        print(response)

    client_menu()


def edit_client_0():
    global ec
    global data
    global ed

    data.clear()

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
    
    if clients_list[ec][0] == 1:
        collection = db.mqtt_clients
    elif clients_list[ec][0] == 2:
        collection = db.http_clients
    elif clients_list[ec][0] == 3:
        collection = db.mongodb_clients

    client = collection.find({"_id" : clients_list[ec][1]})

    data = []
    ctr = 0
    for doc in client:
        for item in doc:
            if ctr == 0:
                ctr = ctr + 1
                continue
            arg = '[' + str(ctr-1) + '] ' + str(item) + ' : ' + str(doc[str(item)])
            print(arg)
            data.append([item, doc[item]])
            ctr = ctr + 1

    print("\nSELECT ITEM TO EDIT")
    edit = input("Enter: ")
    if edit.isdigit() == 0:
        print("Invalid input!\n")
        edit_client_0()
    if int(edit) < -1 or int(edit) > len(data)-1:
        print("Invalid input!\n")
        edit_client_0()

    ed = int(edit)
    edit_client_1(clients_list[ec][1])

    # delete item from collection
    # add client based on new list.... according to designated collection


def edit_client():
    global ec
    print_clients()
    print("SELECT A CLIENT TO EDIT")
    sel = input("Enter: ") # Selection
    print('')
    if sel.isdigit() == 0:
        print("Invalid input!\n")
        edit_client()
    if int(sel) < -1 or int(sel) > len(clients_list)-1:
        print("Invalid input!\n")
        edit_client()

    ec = int(sel)
    edit_client_0()


def client_adder_mongodb():
    print("ADD PUBLISHING CLIENT USING MONGODB AS GATEWAY/BROKER")
    md = open(MDBp, 'r')
    for line in md:
        print(line.strip('\n'))
    md.close()

    care1_device_id = ""
    care1_device_id = input("CARE1 Device ID (press ENTER if no ID): ")
    connection_str = ""
    connection_str = input("Connection String (URI): ")
    print("Select IPE protocol")
    print("[0] HTTP")
    print("[1] MQTT")
    sel = input("Enter: ")
    if sel == '0':
        protocol = "HTTP"
    elif sel == '1':
        protocol = "MQTT"
    else:
        print("Invalid input!\n")
        client_adder_mongodb()

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
    collection = db.mongodb_clients

    post = {
        "care1_device_id" : care1_device_id,
        "URI" : connection_str,
        "protocol" : protocol
    }

    post_id = collection.insert_one(post).inserted_id
    response = "\nClient " + str(post_id) + " successfully added."
    print(response)
    client_menu()


def client_adder_MQTTp():
    print("ADD MQTT PUBLISHING CLIENT")
    mq = open(MQTTp, 'r')
    for line in mq:
        print(line.strip('\n'))
    mq.close()

    care1_device_id = ""
    care1_device_id = input("CARE1 Device ID (press ENTER if no ID): ")
    broker = input("Broker URL: ")
    port = input("Port number: ")
    username = ""
    username = input("Username (press ENTER if no username): ")
    pw = ""
    pw = input("Password (press ENTER if no password): ")
    n_topics = 0
    n_topics = int(input("Number of topics (if editing later, type '0'): "))
    topic_str = []
    qos = []

    if n_topics != 0:
        for i in range(n_topics):
            arg = "Topic String " + str(i+1) + ": "
            topic_str.append(input(arg))
            qos.append(int(input("Quality of Service (QOS): ")))
    else:
        print("Topics are to be added later.")

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
    collection = db.mqtt_clients

    topics = []
    for i in range(n_topics):
        topics.append([topic_str[i], qos[i]])

    post = {
        "care1_device_id" : care1_device_id,
        "broker" : broker,
        "port" : port,
        "username" : username,
        "password" : pw,
        "type" : "PUB",
        "topics" : topics
    }

    post_id = collection.insert_one(post).inserted_id
    response = "\nClient " + str(post_id) + " successfully added."
    print(response)
    client_menu()


def client_adder_MQTTs():
    print("ADD MQTT SUBSCRIBING CLIENT")
    mq = open(MQTTs, 'r')
    for line in mq:
        print(line.strip('\n'))
    mq.close()

    care1_device_id = ""
    care1_device_id = input("CARE1 Device ID (press ENTER if no ID): ")
    broker = input("Broker URL: ")
    port = input("Port number: ")
    username = ""
    username = input("Username (press ENTER if no username): ")
    pw = ""
    pw = input("Password (press ENTER if no password): ")
    n_topics = 0
    n_topics = int(input("Number of topics: "))
    topic_str = []
    qos = []
    for i in range(n_topics):
        arg = "Topic String " + str(i+1) + ": "
        topic_str.append(input(arg))
        qos.append(int(input("Quality of Service (QOS): ")))

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
    collection = db.mqtt_clients

    topics = []
    for i in range(n_topics):
        topics.append([topic_str[i], qos[i]])

    post = {
        "care1_device_id" : care1_device_id,
        "broker" : broker,
        "port" : port,
        "username" : username,
        "password" : pw,
        "type" : "SUB",
        "topics" : topics
    }

    post_id = collection.insert_one(post).inserted_id
    response = "\nClient " + str(post_id) + " successfully added."
    print(response)
    client_menu()


def client_adder_HTTPp():
    print("HERE")


def client_adder_HTTPs():
    print("HERE")


def add_client():
    print_clients()
    print("ADD CLIENTS - Actions:")
    print("[1] Add MQTT Publisher (sensor IPEs)")
    print("[2] Add MQTT Subscriber (actuator IPEs, MQTT GUI)")
    print("[3] Add HTTP Posting Client (sensor IPEs)")
    print("[4] Add HTTP Requesting Client (actuator IPEs, HTTP GUI)")
    print("[5] Add MongoDB Publishing/Posting Client (HTTP/MQTT sensor IPES with MongoDB as gateway/broker)")
    print('')
    action = input("Enter: ")
    print('')
    if action == '1':
        client_adder_MQTTp()
    elif action == '2':
        client_adder_MQTTs()
    elif action == '3':
        client_adder_HTTPp()
    elif action == '4':
        client_adder_HTTPs()
    elif action == '5':
        client_adder_mongodb()
    else:
        print("Invalid input!\n")
        add_client()


def remove_client():
    print_clients()
    global clients_list
    remove = input("Remove: ")
    if remove.isnumeric():
        n = int(remove)
        if n > len(clients_list)-1 or n < 0:
            print("Invalid input!\n")
            remove_client()
        else:
            c = clients_list.pop(n)

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

            if c[0] == 1:
                collection = db.mqtt_clients
            elif c[0] == 2:
                collection = db.http_clients
            elif c[0] == 3:
                collection = db.mongodb_clients
            collection.delete_one({"_id" : c[1]})
            client_menu()
    else:
        print("Invalid input!\n")
        remove_client()


def client_menu():
    print_clients()
    print("Actions:")
    print("[1] Add client")
    print("[2] Remove client")
    print("[3] Edit client")
    print('')
    action = input("Enter: ")
    print('')
    if action == '1':
        add_client()
    elif action == '2':
        remove_client()
    elif action == '3':
        edit_client()
    else:
        print("Invalid input!\n")
        client_menu()


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


def install_dependencies():
    print("Installing dependencies...")
    commands = ['pip install requests',
                'pip install pymongo',
                'pip install python-dotenv',
                'pip install paho-mqtt']
    for item in commands:
        dep = subprocess.run(item, shell=True, capture_output=True)
        print(dep.stdout.decode())

    
def start():
    # Terms and Conditions
    tnc = open(terms, "r")
    for line in tnc:
        print(line.strip('\n'))
    tnc.close()

    # Install dependencies
    print("\nSkip installation of dependencies? (y/n)")
    dep = input("\nEnter: ")
    if dep == 'y' or dep == 'Y':
        print("\nSkipping installation of dependencies.\n")
    else:
        install_dependencies()


    # MongoDB configuration
    from dotenv import load_dotenv, find_dotenv
    import os
    import pprint
    from pymongo import MongoClient
    load_dotenv(find_dotenv())
    password = os.environ.get("MONGODB_PW")
    connection_string = f"mongodb+srv://care1:{password}@care1.yf7ltcy.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
        
    client_menu()


start()