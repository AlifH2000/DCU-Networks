# To get started I used https://fastapi.tiangolo.com/tutorial/first-steps/ for help
# Importing FASTAPI
from fastapi import FastAPI, Request
from pydantic import BaseModel

description = """
By Alif Hossain

## Introduction
This assignment consists of an IP calculator, A subnet calculator and a supernet Calculator.

## Functions
The main functions used in this assignment are for the 3 calculator:
- The main function of **"/ipcalc"**(ip calculator) is to take an ip address and execute it in order to determinate what network class it belongs to.
- The main function of **"/subnet"**(subnet calculator) is to take in both an ip address and a mask address. Basically, you give the Subnet Calculator a range of IP addresses or CIDR notations and it calculates/generates a list of subnets for you.
- The main function of **Supernet** Calculator is to create a supernet from one or more provided subnet or network addresses.
- The **"decimal_to_binary"** function allows the subnet calculator to change decimal values in to binary.

## Input & Descriptions
- **"IP : string"** = is an input which askes for an ip address.
- **"mask : string"** = is an input which askes for a mask address.

## Output and Descriptions
\n
- For **"/ipcalc"** the output is =\n 
  "class": "B",\n
  "num_networks": 16384,\n
  "num_hosts": 65536,/n
  "first_address": "128.0.0.0",\n
  "last_address": "191.255.255.255"\n

- For **"/subnet"** the output is:
  "address_cidr": "192.168.10.0/26",\n
  "num_subnets": 4,\n
  "addressable_hosts_per_subnet": 62,\n
  "valid_subnets": [
    "192.168.10.0",
    "192.168.10.64",
    "192.168.10.128",
    "192.168.10.192"
  ],\n
  "broadcast_addresses": [
    "192.168.10.0",
    "192.168.10.64",
    "192.168.10.128",
    "192.168.10.192"
  ],\n
  "first_addresses": [
    "192.168.10.0",
    "192.168.10.64",
    "192.168.10.128",
    "192.168.10.192"
  ],\n
  "last_addresses": [
    "192.168.10.0",
    "192.168.10.64",
    "192.168.10.128",
    "192.168.10.192"
  ]\n

"""

# Using FASTAPI
app = FastAPI(title="CA304 Network Assignment 1",
    description=description,
    version="0.0.1", contact={
        "name": "Alif Hossain", "email": "alif.hossain5@mail.dcu.ie",
    },)

class Informations(BaseModel):
    IP : str
    mask : str
# using ".get()" to provide a message.

@app.get("/")
async def description():
    return {"message": "This is an IP catculator"}

# The first part writes an endpoint called ipcalc that takes in JSON from a post request. The endpoint will take in a JSON object containing an IP address in decimal dot notation.
# Using ".post()" to write a ipcalc function.

@app.post("/ipcalc")
async def get_body(var: Informations):
    answer = var.IP.split(".")
    return both_ip(answer)

# used https://www.geeksforgeeks.org/program-determine-class-network-host-id-ipv4-address/ to differenciate between the different classes
def both_ip(answer):
  if(int(answer[0]) >= 0 and int(answer[0]) <= 127):
    return{
  "class": "A",
  "num_networks": 127,
  "num_hosts": 16777214,
  "first_address": "1.0.0.0",
  "last_address": "127.255.255.255"
}
   
  elif(int(answer[0]) >=128 and int(answer[0]) <= 191):
    return{
  "class": "B",
  "num_networks": 16384,
  "num_hosts": 65536,
  "first_address": "128.0.0.0",
  "last_address": "191.255.255.255"
}

  elif(int(answer[0]) >= 192 and int(answer[0]) <= 223):
    return{
  "class": "C",
  "num_networks": 2097152,
  "num_hosts": 254,
  "first_address": "192.0.0.0",
  "last_address": "223.255.255.255"
}
# KEY: 
# Class D and class E addresses should return "N/A" for the num_hosts and num_networks field. 

  elif(int(answer[0]) >= 224 and int(answer[0]) <= 239):
    return{
  "class": "D",
  "num_networks": "N/A",
  "num_hosts": "N/A",
  "first_address": "224.0.0.0",
  "last_address": "239.255.255.255"
}

  else:
    return{
  "class": "E",
  "num_networks": "N/A",
  "num_hosts": "N/A",
  "first_address": "240.0.0.0",
  "last_address": "255.255.255.254"
}

@app.get("/")
async def description():
    return {"message": "This is a Subnet catculator"}

# The "/subnet" function writes an endpoint called subnet which will take in a class C or class B address and a subnet mask.
@app.post("/subnet")
async def get_body(var: Informations):
    ip_address = var.IP.split(".")
    endpoint = var.mask.split(".")
    return mask_for_subnet(ip_address, endpoint)

def mask_for_subnet(ip_address, endpoint):
    return{
    # The endpoint will return the following json structure.
	"address_cidr" : address_in_cidr(ip_address, endpoint),
	"num_subnets": number_of_subnets(ip_address, endpoint),
	"addressable_hosts_per_subnet": addressable_hosts(endpoint),
	"valid_subnets": valid_subnets(ip_address, endpoint),
	"broadcast_addresses": broadcast_addresses(ip_address, endpoint),
	"first_addresses": first_add(ip_address, endpoint),
	"last_addresses": last_add(ip_address, endpoint),
}

# This converter that changes decimal values in binary.
def decimal_to_binary(endpoint):
    tmp = [] # Use an empty list
    for value in endpoint:
        if value == "0":
            tmp.append("00000000")
        else:
            change = bin(int(value))
            change = change[2:]
            tmp.append(change)
    Total = ".".join(tmp)
    # Add it to the total at the end
    return Total

def all_ones(endpoint):
    in_binary = decimal_to_binary(endpoint)
    a = 0
    for n in in_binary:
        if n == "1":
            # If it equates to 1 add one to a everytime.
            a = a + 1
    return a

#This provides the "address_cidr" result
def address_in_cidr(ip_address, endpoint):
    cidr_notation = str(all_ones(endpoint))
    return ".".join(ip_address) + "/" + cidr_notation

def number_of_subnets(ip_address, endpoint):
    a = all_ones(endpoint)
    if int(ip_address[0]) >= 192 and int(ip_address[0]) <=223:
        x = a - 24
    else:
        x = a - 24
    all_networks = 2 ** x
    return all_networks

def all_zeros(endpoint):
    in_binary = decimal_to_binary(endpoint)
    a = 0
    for i in in_binary:
        if i == "0":
            a = a + 1
    if a == 0:
        a = 1
    return a

def addressable_hosts(endpoint):
    j = (2 ** all_zeros(endpoint))
    count = j - 2
    return count

def valid_subnets(ip_address, endpoint):
    if int(ip_address[0]) >= 128 and int(ip_address[0]) <=191:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + str(a) + "." + ip_address[3])
            a = a + x
            c = c + 1
    else:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + ip_address[2] + "." + str(a))
            a = a + x
            c = c + 1
    return new_list

def broadcast_addresses(ip_address, endpoint):
    if int(ip_address[0]) >= 128 and int(ip_address[0]) <= 191:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + str(a) + "." + ip_address[3])
            a = a + x
            c = c + 1
    else:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + ip_address[2] + "." + str(a))
            a = a + x
            c = c + 1
    return new_list

def first_add(ip_address, endpoint):
    if int(ip_address[0]) >= 128 and int(ip_address[0]) <= 191:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + str(a) + "." + ip_address[3])
            a = a + x
            c = c + 1
    else:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + ip_address[2] + "." + str(a))
            a = a + x
            c = c + 1
    return new_list

def last_add(ip_address, endpoint):
    if int(ip_address[0]) >= 128 and int(ip_address[0]) <= 191:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + str(a) + "." + ip_address[3])
            a = a + x
            c = c + 1
    else:
        new_list = []
        c = 0
        a = 0
        x = 256 // number_of_subnets(ip_address, endpoint)
        while c < number_of_subnets(ip_address, endpoint):
            new_list.append(ip_address[0] + "." + ip_address[1] + "." + ip_address[2] + "." + str(a))
            a = a + x
            c = c + 1
    return new_list