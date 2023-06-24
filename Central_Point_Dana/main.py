#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


import subprocess
from os.path import exists


# Global variables
terms = "src/TERMS_AND_CONDITIONS.txt"
p_client = "src/p_client_note.txt"
s_client = "src/s_client_note.txt"
clients_list = []
ec = 0
data = []
ed = 0


def maintain_cp():
    print("\n\nCENTRAL POINT MAINTENANCE")
    print("\nSelect action:")
    print("[0] ")


def start_client_connect():
    print("\n\nSTART CLIENT CONNECTION")
    print("\nSTART_CLIENT_CONNECT will open a new tab and run the start_client_connect program to start connection in parallel. The program in the current tab will not be terminated. Would you like to proceed? (y/n)")
    s = input("\nEnter: ")
    if s == 'y' or s == 'Y':
        command = "gnome-terminal --tab --title=start_client_connect -- bash -c 'python3 start_client_connect.py ;bash'"
        dep = subprocess.run(command, shell=True, capture_output=True)
        main_menu()
    else:
        print("\n\nReturning to client menu")
        main_menu()


def edit_client_1(eid):
    global ec
    global data
    global ed

    if clients_list[ec][0] == 0:
        collection = main_db.mongodb_clients
        # This section is specifically for MongoDB client_adder
        if ed == 2:
            arg = "\n\n" + str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            print("\nSelect NEW protocol:\n[0] HTTP\n[1] MQTT\n[2] HTTP/MQTT")
            action = input("\nEnter: ")
            if action == '0':
                data[ed][1] = "HTTP"
                print("\n\nClient attribute edited successfully.")
            elif action == '1':
                data[ed][1] = "MQTT"
                print("\n\nClient attribute edited successfully.")
            elif action == '2':
                data[ed][1] = "HTTP/MQTT"
                print("\n\nClient attribute edited successfully.")
            else:
                print("\n\nInvalid input! Type is not changed.\n")
        if ed == 3:
            arg = "\n\n" + str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            print("\nSelect NEW type:\n[0] Publishing\n[1] Subscribing")
            action = input("\nEnter: ")
            if action == '0':
                data[ed][1] = "pub"
                print("\n\nClient attribute edited successfully.")
            elif action == '1':
                data[ed][1] = "sub"
                print("\n\nClient attribute edited successfully.")
            else:
                print("\n\nInvalid input! Type is not changed.\n")
        if ed == 4:
            if data[3][1] == "pub":
                arg = "\n\n" + str(data[ed][0]) + " : " + str(data[ed][1])
                print(arg)
                print("\nSelect NEW device:\n[0] Sensor\n[1] Actuation Switch")
                action = input("\nEnter: ")
                if action == '0':
                    data[ed][1] = "sensor"
                    print("\n\nClient attribute edited successfully.")
                elif action == '1':
                    data[ed][1] = "actuation switch"
                    print("\n\nClient attribute edited successfully.")
                else:
                    print("\n\nInvalid input! Type is not changed.\n")
            elif data[3][1] == "sub":
                arg = "\n\n" + str(data[ed][0]) + " : " + str(data[ed][1])
                print(arg)
                print("\nSelect NEW device:\n[0] Actuator\n[1] Monitoring Application")
                action = input("\nEnter: ")
                if action == '0':
                    data[ed][1] = "actuator"
                    print("\n\nClient attribute edited successfully.")
                elif action == '1':
                    data[ed][1] = "monitoring application"
                    print("\n\nClient attribute edited successfully.")
                else:
                    print("\n\nInvalid input! Type is not changed.\n")
        else:
            arg = "\n\n" + str(data[ed][0]) + " : " + str(data[ed][1])
            print(arg)
            arg = "\nEnter NEW " + str(data[ed][0]) + ": "
            new = input(arg)
            if new != '\n' or new != '':
                data[ed][1] = new.strip('\n')
                print("\n\nClient attribute edited successfully.")

        # Modifying in MongoDB
        post = {
            "_id" : eid,
            "care1_device_id" : data[0][1],
            "URI" : data[1][1],
            "protocol" : data[2][1],
            "type" : data[3][1]
        }
        newval = { "$set": post }
        collection.update_one({"_id" : eid}, newval)
        response = "\n\nClient successfully modified with id " + str(eid) + "."
        print(response)

    main_menu()


def edit_client_0():
    global ec
    global data
    global ed

    data.clear()
    
    if clients_list[ec][0] == 0:
        collection = main_db.mongodb_clients

    client = collection.find({"_id" : clients_list[ec][1]})

    data = []
    ctr = 0
    print("\n\n")
    for doc in client:
        for item in doc:
            if ctr == 0:
                ctr = ctr + 1
                continue
            arg = '[' + str(ctr-1) + '] ' + str(item) + ' : ' + str(doc[str(item)])
            print(arg)
            data.append([item, doc[item]])
            ctr = ctr + 1

    print("\n\nSELECT ITEM TO EDIT")
    edit = input("\nEnter: ")
    if edit.isdigit() == 0:
        print("\n\nInvalid input!\n")
        edit_client_0()
    if int(edit) < -1 or int(edit) > len(data)-1:
        print("\n\nInvalid input!\n")
        edit_client_0()

    ed = int(edit)
    edit_client_1(clients_list[ec][1])


def edit_client():
    print("\n\nEDIT CLIENT")
    global ec
    print_clients()
    sel = input("\nSelect client to edit: ")
    print('')
    if sel.isdigit() == 0:
        print("\n\nInvalid input!\n")
        edit_client()
    if int(sel) < -1 or int(sel) > len(clients_list)-1:
        print("\n\nInvalid input!\n")
        edit_client()

    ec = int(sel)
    edit_client_0()


def client_adder(type):
    if type == 0:
        print("\n\nADD PUBLISHING CLIENT")
        md = open(p_client, 'r')
        t = "pub"
        print("\nSelect device")
        print("[0] Sensor")
        print("[1] Actuation Switch")
        sel = input("\nEnter: ")
        if sel == '0':
            device = "sensor"
        elif sel == '1':
            device = "actuation switch"
        else:
            print("\n\nInvalid input!\n")
            client_adder()
    if type == 1:
        print("\n\nADD SUBSCRIBING CLIENT")
        md = open(s_client, 'r')
        t = "sub"
        print("\nSelect device")
        print("[0] Actuator")
        print("[1] Monitoring Application")
        sel = input("\nEnter: ")
        if sel == '0':
            device = "actuator"
        elif sel == '1':
            device = "monitoring application"
        else:
            print("\n\nInvalid input!\n")
            client_adder()

    for line in md:
        print(line.strip('\n'))
    md.close()

    care1_device_id = ""
    care1_device_id = input("\nCARE1 Device ID (press ENTER if no ID): ")
    connection_str = ""
    connection_str = input("\nConnection String (URI): ")
    print("\nSelect protocol")
    print("[0] HTTP")
    print("[1] MQTT")
    print("[2] HTTP/MQTT")
    sel = input("\nEnter: ")
    if sel == '0':
        protocol = "HTTP"
    elif sel == '1':
        protocol = "MQTT"
    elif sel == '2':
        protocol = "HTTP/MQTT"
    else:
        print("\n\nInvalid input!\n")
        client_adder_mongodb()

    collection = main_db.mongodb_clients

    post = {
        "care1_device_id" : care1_device_id,
        "URI" : connection_str,
        "protocol" : protocol,
        "type" : t,
        "device" : device
    }

    db1 = main_client.mongodb_client_readings
    db1.create_collection(care1_device_id)

    post_id = collection.insert_one(post).inserted_id
    response = "\n\nClient " + str(post_id) + " successfully added."
    print(response)
    main_menu()


def add_client():
    print("\n\nADD CLIENT")
    print_clients()
    print("\n\nSelect action:")
    print("[0] Add Publishing Client (sensors, actuator switches, etc.)")
    print("[1] Add Subscribing Client (actuators, monitoring applications, etc.)")
    action = input("\nEnter: ")
    if action == '0':
        client_adder(0)
    elif action == '1':
        client_adder(1)
    else:
        print("\n\nInvalid input!\n")
        add_client()


def remove_client():
    print("\n\nREMOVE CLIENT")
    print_clients()
    global clients_list
    remove = input("\nRemove: ")
    if remove.isnumeric():
        n = int(remove)
        if n > len(clients_list)-1 or n < 0:
            print("\n\nInvalid input!\n")
            remove_client()
        else:
            c = clients_list.pop(n)
            if c[0] == 0:
                collection = main_db.mongodb_clients
            collection.delete_one({"_id" : c[1]})
            main_menu()
    else:
        print("\n\nInvalid input!\n")
        remove_client()


def print_clients():
    collection = main_db.mongodb_clients
    global clients_list
    clients_list.clear()

    print("\n\nEXISTING CLIENTS")
    ctr = 0
    for doc in collection.find():
        post = '[' + str(ctr) + ']' + " - [" + doc["type"] + '] ' + doc["care1_device_id"] + '-' + doc["device"]
        print(post)
        clients_list.append([0, doc["_id"]])
        ctr = ctr + 1


def main_menu():
    print("\n\nMAIN MENU")
    print_clients()
    print("\n\nSelect action:")
    print("[0] Add client")
    print("[1] Remove client")
    print("[2] Edit client")
    print("[3] Start sensor/actuator client connect")
    print("[4] Central point maintainance")
    action = input("\nEnter: ")
    if action == '0':
        add_client()
    elif action == '1':
        remove_client()
    elif action == '2':
        edit_client()
    elif action == '3':
        start_client_connect()
    elif action == '4':
        maintain_cp()
    else:
        print("\n\nInvalid input!\n")
        main_menu()


def install_dependencies():
    print("\n\nInstalling dependencies...")
    commands = ['pip install requests',
                'pip install pymongo',
                'pip install python-dotenv']
    print("\n\n")
    for item in commands:
        dep = subprocess.run(item, shell=True, capture_output=True)
        print(dep.stdout.decode())

    
# START


# Terms and Conditions
tnc = open(terms, "r")
for line in tnc:
    print(line.strip('\n'))
tnc.close()


# Install dependencies
print("\n\nSkip installation of dependencies? (y/n)")
dep = input("\nEnter: ")
if dep == 'y' or dep == 'Y':
    print("\n\nSkipping installation of dependencies.\n")
else:
    install_dependencies()


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
    

main_menu()