from fastapi import FastAPI
from pydantic import BaseModel, Field


description = """
By Alif Hossain

## Introduction
I created a mock router using FastAPI

## Functions

addrouter - The "addrouter" function is an endpoint that takes in JSON from a post request. It takes in a JSON ocject that has the name of the router and adds it to my graph.\n
adding_rout - The "adding_rout" function allows you to add new routers to an existing list and graph-ing it. It takes the first router and the second router and the distance between them in the form of ("weight") to determine wether its a new connection or does a node already exists.\n
connect - The "connect" function  is an endpoint that takes in a JSON from a POST request. It takes 2 routers in this case "A" and "B" plus the distance between them("weight").\n
removerouter - The "removerouter" function is an endpoint that takes in a JSON from a POST request. It takes the "name" of the router and removes it from the graph.\n
removeconnection - The "removerouter" function is an endpoint that takes in JSON data from a POST request containing the names of two routers. It also removes any connection between the two routers from the graph.\n
route - The "route" function is an endpoint that takes in JSON from a post request which returns the shortest path between two routers in the graph.\n 
The endpoint takes in the names of two routers (from and to ) and returns:
<li> -The total weight of the route between the two routers.</li>\n
<li> -A list of the connections in order which provide the route between the two.</li>

## Input & Descriptions


        {"name": "A"} = Input for "addrouter"\n
        {"from": "A", "to": "B", "weight": 5} = Input for "connect"\n
        {"name": "A"}   =   Input for "removerouter"\n
        {"time_from": "string", "to": "string"}   =   Input for "removeconnection"\n
        {"time_from": "string", "to": "string"}  =  Input for "route"\n



## Output and Descriptions

        {"status": "success"} = Output for "addrouter"\n
        {"status": "Error, router does not exist"} = Output for "connect"\n
        null = Output for "removerouter"\n

## An example of an input and output

        {"name": "string"} = Input for "addrouter"\n
        {"status": "success"} = Output for "addrouter"\n


"""
# Using FASTAPI
app = FastAPI(title="CA304 Network Assignment 2",
    description=description, contact={
        "name": "Alif Hossain", "email": "alif.hossain5@mail.dcu.ie",
    },)

endpoints = {}#Creating a graph
class New_R(BaseModel):
    name: str

@app.post("/addrouter/")# Adds a new router to the graph
def addrouter(detail : New_R):
    newR_info = detail.name
    return adding_rout(newR_info)

all_routs = []
def adding_rout(newR_info):#Returns wether or not it was successful or not.
    if newR_info not in all_routs:
        all_routs.append(newR_info)
        return {
            "status": "success"
        }
    else:
        return {
            "status": "Error, node already exists"
        }

class Two_Routers(BaseModel):
    time_from: str = Field(None, alias="from") # Reference: https://stackoverflow.com/questions/69306103/is-it-possible-to-change-the-output-alias-in-pydantic 
    to: str
    weight: int

@app.post("/connect/")
def connect(details_1: Two_Routers):# The connect Function check wether a connection exists or not between 2 routers and updates the graph afterwards.
    A_data = details_1.time_from
    B_data = details_1.to
    weight = details_1.weight
    if (A_data or B_data) not in endpoints:#checks to see if a connection exists.
        return{
            "status": "Error, router does not exist"
        }
    else:
        Total_rotations = 0
        first_connection = [A_data, weight]
        second_connection = [B_data, weight]
        for imp, data in endpoints.items():
            if imp == A_data:#used an if loop within
                add_connection = []
                a = 0
                while a < len(data):#create a while loop
                    first_list = data[a]
                    if (first_list[0] == B_data) and (first_list[1] != weight):
                        add_connection.append(first_list[0])
                        add_connection.append(weight)
                        data[a] = add_connection
                        Total_rotations = Total_rotations + 1
                    else:
                        Total_rotations = Total_rotations + 1
                    a = a + 1
            elif imp == B_data:
                add_connection = []
                b = 0
                while b < len(data):
                    second_list = data[b]
                    if (second_list[0] == A_data) and (second_list[1] != weight):
                        add_connection.append(second_list[0])# appending to the list.
                        add_connection.append(weight)
                        data[b] = add_connection
                        Total_rotations = Total_rotations + 1
                    else:
                        Total_rotations = Total_rotations + 1
                    b = b + 1

        if Total_rotations == 0:
            endpoints[A_data].append(second_connection)
            endpoints[B_data].append(first_connection)
            return {
                "status": "success"
            }
        else:
            return {
                "status": "updated"
            }# if no previous connection it prints success or else updated on the graph.

class Router_remove(BaseModel):
    name: str

@app.post("/removerouter/")
def removerouter(details_2: Router_remove):# The remove router function reomoves a router from the graph.
    newR_info = details_2.name
    if newR_info not in endpoints:
        pass
    else:
        endpoints.pop(newR_info)#used .pop() to remove a router from the graph.
        for imp, data in endpoints.items():
            a = 0
            while a < len(data):
                b = data[a]
                if b[0] == newR_info:
                    del data[a]# used a del function
                a = a + 1
        return endpoints.items()

class Connection_remove(BaseModel):
    time_from: str
    to: str

@app.post("/removeconnection/")
def removeconnection(details_3: Connection_remove):#This removes a connection from the graph.
    start = details_3.time_from
    finish = details_3.to
    for imp, data in endpoints.items():
        if imp == start:
            a = 0
            while a < len(data):
                b = data[a]
                if b[0] == finish:
                    del data[a]
                a = a + 1
        elif imp == finish:
            c = 0
            while c < len(data):
                d = data[c]
                if d[0] == start:
                    del data[c]
                c = c + 1
    return endpoints.items()

class Shortest_path(BaseModel):# This class has 2 inputs from and to both are string.
    time_from: str
    to: str

@app.post("/route/")
def route(details_4: Shortest_path):#creating a route function that measures the shortest distance between 2 routers.
    start = details_4.time_from
    finish = details_4.to
