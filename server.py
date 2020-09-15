import asyncio
import datetime
import random
import websockets
import socket
import pandas
import threading
import time
import numpy as np
import json

ip = socket.gethostbyname(socket.gethostname())
print(ip)
sep = ";"
waitTime = 0.5

#dataQueue = []
inUseData = []



async def timeg(websocket, path):
    while True:
        if len(inUseData)>0:
            data = fixData(inUseData[0])
            await websocket.send(data)
            await asyncio.sleep(waitTime)
        else:
            await websocket.send("0")
            await asyncio.sleep(0.5)
        
def fixData(data):
    a = "{"
    a+= "\"latitude\":\""             +str(data[0])+"\","
    a+= "\"longitude\":\""            +str(data[0])+"\","
    a+= "\"Altitude\":\""             +str(data[0])+"\","
    a+= "\"falling\":\""              +str(data[0])+"\","
    a+= "\"Temperature_1\":\""        +str(data[0])+"\","
    a+= "\"Temperature_2\":\""        +str(data[0])+"\","
    a+= "\"Barometric_Pressure\":\""  +str(data[0])+"\","
    a+= "\"pitch\":\""                +str(data[0])+"\","
    a+= "\"rueda\":\""                +str(data[0])+"\","
    a+= "\"yaw\":\""                  +str(data[0])+"\","
    a+= "\"Accelerometer_X\":\""      +str(data[0])+"\","
    a+= "\"Accelerometer_Y\":\""      +str(data[0])+"\","
    a+= "\"Accelerometer_Z\":\""      +str(data[0])+"\""
    a+="}"
    return a

def sendData(data):
    dataQueue.append(data)

def connect():
    start_server = websockets.serve(timeg, ip, 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def setData():
    readCSV()

def readCSV():
    df = pandas.read_csv('data.csv',sep=sep)
    global dataQueue
    dataQueue = df.to_numpy()
    

def prepareData():
    global dataQueue
    time.sleep(waitTime+2)    
    while True:
        inUseData.clear()
        if len(dataQueue)>0:
            inUseData.append(dataQueue[0])
            dataQueue = dataQueue[1:]
        time.sleep(waitTime)

def dummy():
    ts = threading.Thread(target=setData)
    ts.start()

def start():
    tg = threading.Thread(target=prepareData)
    tg.start()

def listen():
    connect()

dummy()
start()
listen()