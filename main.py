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
clients_list = []

def client_adder_MQTTp():
    print("HERE")


    print("Client successfully added.")
    client_menu()


def client_adder_MQTTs():
    print("HERE")


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
    else:
        print("Invalid input!\n")
        add_client()


def remove_client():
    print_clients()
    global clients_list
    print(clients_list)
    print(len(clients_list))
    remove = input("Remove: ")
    if remove.isnumeric():
        n = int(remove)
        if n > len(clients_list)-1 or n < 0:
            print("Invalid input!\n")
            remove_client()
        else:
            clients_list.pop(n)
            cli = open(clients, 'w')
            for i in clients_list:
                cli.write(i + '\n') # change format / way of writing based on clients_list format / type
            cli.close()
            client_menu()
    else:
        print("Invalid input!\n")
        remove_client()


def client_menu():
    print("Actions:")
    print("[1] Add client")
    print("[2] Remove client")
    print('')
    action = input("Enter: ")
    print('')
    if action == '1':
        add_client()
    elif action == '2':
        remove_client()
    else:
        print("Invalid input!\n")
        client_menu()


def print_clients():
    if exists(clients):
        print("Existing clients:")
        global clients_list
        clients_list.clear()
        cli = open(clients, "r")
        ctr = 0
        for line in cli:
            print(str(ctr), ': ', line.strip('\n'), sep = '')
            clients_list.append(line.strip('\n'))
            ctr = ctr + 1
        print('')
        cli.close()
    else:
        cli = open(clients, "w")
        cli.close()


def install_dependencies():
    print("Installing dependencies.")
    commands = ['pip install requests',
                'pip install pymongo',
                'pip install python-dotenv']
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
        
        
    # Print clients
    print_clients()
    client_menu()


start()

'''
Next steps

- Register publishing clients (HTTP, MQTT)
    - Ask for device (collection) name
    - Create 1 collection per client
- Create insert_docs function
- Parallelized:
    - Subscribe/get requests from clients in realtime (loop)
    - While on loop, run insert_docs

- Register subscribing clients (HTTP, MQTT)
- Create get_docs function
- Parallelized:
    - Retrieve documents from collections and publish to clients
'''