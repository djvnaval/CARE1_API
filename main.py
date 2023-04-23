#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:25:32 2023

@author: dana
"""


import subprocess
from os.path import exists


# Global variables
clients = "logs/clients.txt"
runs = "logs/runs.txt"
clients_list = []


def add_client():
    print("HERE")


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
            print('[', str(ctr), '] ', line.strip('\n'), sep = '')
            clients_list.append(line.strip('\n'))
            ctr = ctr + 1
        print('')
        cli.close()
    else:
        cli = open(clients, "w")
        cli.close()


def install_dependencies():
    print("Installing dependencies.")
    dep = subprocess.run('pip install requests', shell=True, capture_output=True)
    print(dep.stdout.decode())
    

def start():
    # Install dependencies
    if exists(runs):
        run = open(runs, "r")
        n = int(run.read())
        run.close()

        run = open(runs, "w")
        run.write(str(n+1))
        run.close()

        print("Runs:", str(n), '\n')
    else:
        # Initialize counter for runs
        run = open(runs, "w")
        run.write("1")
        run.close()
        install_dependencies()
        
    # Print clients
    print_clients()
    client_menu()


start()
