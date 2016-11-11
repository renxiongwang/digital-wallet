import numpy as np
import pandas as pd
import math as m
import matplotlib as plt
import datetime
import sys

global inputDirect1, inputDirect2
global outputDirect1, outputDirect2, outputDirect3

inputDirect1 = str(sys.argv[1])
inputDirect2 = str(sys.argv[2])
outputDirect1 = str(sys.argv[3])
outputDirect2 = str(sys.argv[4])
outputDirect3 = str(sys.argv[5])

batch = open(inputDirect1,"r")
batchPayment = batch.readlines()
stream = open(inputDirect2, "r")
streamPayment = stream.readlines()

global degreeMap
global neighborMap

degreeMap = {}
neighborMap = {}

def BFS(id1, id2, degree1, degree2):
    if id1 == id2 or degree1 == 0:
        return;
    if (id1, id2) in degreeMap.keys() and degreeMap[(id1, id2)] == degree2:
        return
    else:
        if degree2 == 1:
            neighborMap[id1].add(id2)
            neighborMap[id2].add(id1)
        if (id1, id2) in degreeMap.keys():
            degreeMap[(id1, id2)] = min(degree2, degreeMap[(id1, id2)])
            degreeMap[(id2, id1)] = min(degree2, degreeMap[(id1, id2)])
        else:
            degreeMap[(id1, id2)] = degree2
            degreeMap[(id2, id1)] = degree2
        for neighbor in neighborMap[id1]:
            BFS(neighbor, id2, degree1 - 1, degree2 + 1)
        for neighbor in neighborMap[id2]:
            BFS(neighbor, id1, degree1 - 1, degree2 + 1)
    return

def update(id1, id2):
    if id1 not in neighborMap.keys():
        neighborMap[id1] = set()
    if id2 not in neighborMap.keys():
        neighborMap[id2] = set()
    BFS(id1, id2, 4, 1);
    return

def isValid1(id1, id2):
    if id1 == id2:
        return "trusted\n"
    if (id1, id2) in degreeMap.keys() and degreeMap[(id1, id2)] == 1:
        return "trusted\n"
    else:
        return "unverified\n"

def isValid2(id1, id2):
    if id1 == id2:
        return "trusted\n"
    if (id1, id2) in degreeMap.keys() and degreeMap[(id1, id2)] <= 2:
        return "trusted\n"
    else:
        return "unverified\n"

def isValid3(id1, id2):
    if id1 == id2:
        return "trusted\n" 
    if (id1, id2) in degreeMap.keys() and degreeMap[(id1, id2)] <= 4:
        return "trusted\n"  
    else:
        return "unverified\n"
                                    
def readBatch():
    for i in range(1, len(batchPayment)):
	id1 = int(batchPayment[i].split(",")[1])
        id2 = int(batchPayment[i].split(",")[2])
        update(id1, id2)
    return    

def updateStream():
    f1 = open(outputDirect1, 'w')
    f2 = open(outputDirect2, 'w')
    f3 = open(outputDirect3, 'w')
    for i in range(1, len(streamPayment)):
        id1 = int(streamPayment[i].split(",")[1])
        id2 = int(streamPayment[i].split(",")[2])
        f1.write(isValid1(id1, id2))
        f2.write(isValid2(id1, id2))
        f3.write(isValid3(id1, id2))   
    f1.close()
    f2.close()
    f3.close()
    return

readBatch()

updateStream()
