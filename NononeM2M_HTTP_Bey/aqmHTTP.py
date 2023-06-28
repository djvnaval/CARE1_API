from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler

import logging 
import time
import random
import datetime
from inputimeout import inputimeout
from random_object_id import generate
from bson import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://HTTPSystem:HTTPnonOneM2M@nononem2m.lold0yl.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Collections/sensors
db = client.HTTPAQM
#dbActuate = client.HTTPAQM_actuate
colHumi = db.dht22Humi
colTemp = db.dht22Temp
colPM2_5in = db.PM2_5_indoor
colPM2_5out = db.PM2_5_outdoor
colWindow = db.windowSensor
colFilter = db.filterFanSensor

colWinAct = db.windowSensor_actuate
colffAct = db.filterFanSensor_actuate

# Setup logging to the Systemd Journal
log = logging.getLogger('aqm')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

#Gauges for the sensor
gHumidity = Gauge('dht22_humidity', 'Humidity percentage measured by the DHT22 Sensor')
gTemperature = Gauge('dht22_temperature', 'Temperature measured by the DHT22 Sensor')
gPM25in = Gauge('PM2_5_sensor_indoor', 'Air quality basis')
gPM25out = Gauge('PM2_5_sensor_outdoor', 'Air quality basis')
gwindowSensor = Gauge('window_sensor', 'signals whether window is open or not')
gffSensor = Gauge('filterfanSensor', 'sensor to note wheter filter fan is turned on')

def timeStamper():
    timeStamp = datetime.datetime.now()
    return timeStamp

def sleep(seconds):
    time.sleep(seconds)

def getActuationData():
    global winAct
    global ffAct
    
    cursorA = colWinAct.find_one({}, sort=[('time', -1)])
    cursorB = colffAct.find_one({}, sort=[('time', -1)])

    if cursorA == None:
        winAct = 0
    else:
        winAct = cursorA["value"]
    
    if cursorB == None:
        ffAct = 0
    else:
        ffAct = cursorB["value"]
    
    actUpdate()

def pm25indoor(rate):
    global PM2_5in
    #PM2_5in = random.randint(50,60)

    PM2_5in =  PM2_5in + rate
    sleep(0.3)

def pm25outdoor(rate):
    global PM2_5out
    #PM2_5out = random.randint(70,80)

    PM2_5out = PM2_5out + rate
    sleep(0.3)

def dht22Humi():
    humidity = random.randint(30,50)

    dht22SensorHumi = {
            "value":humidity,
            "type":"humidity",
            "unit":"%",
            "time":timeStamper()
            }
    
    colHumi.insert_one(dht22SensorHumi)
    gHumidity.set(humidity)

    return humidity

def dht22Temp():
    temperature = random.randint(34,38)

    dht22SensorTemp = {
            "value":temperature,
            "type":"temperature",
            "unit":"°C",
            "time":timeStamper()
            }
    
    colTemp.insert_one(dht22SensorTemp)
    gTemperature.set(temperature)

    return temperature

def PMin():
    global PM2_5in
    #PM2_5in = random.randint(34,38)

    PM2_5Sensor = {
            "value":PM2_5in,
            "type":"PM2.5",
            "unit":"μg/m3",
            "time":timeStamper()
            }
    
    colPM2_5in.insert_one(PM2_5Sensor)
    gPM25in.set(PM2_5in)

    return PM2_5in

def PMout():
    global PM2_5out
    #PM2_5out = random.randint(34,38)

    PM2_5Sensor = {
            "value":PM2_5out,
            "type":"PM2.5",
            "unit":"μg/m3",
            "time":timeStamper()
            }
    
    colPM2_5out.insert_one(PM2_5Sensor)
    gPM25out.set(PM2_5out)

    return PM2_5out

def windowActuation():
    global winAct
    getActuationData()

    windowSensor = {
        "value":winAct,
        "type":"window sensor",
        "unit":"none",
        "time":timeStamper()
    }

    colWindow.insert_one(windowSensor)
    gwindowSensor.set(winAct)

    return winAct

def filterfanActuation():
    global ffAct
    getActuationData()

    ffSensor = {
        "value":ffAct,
        "type":"filter fan sensor",
        "unit":"none",
        "time":timeStamper()
    }

    colFilter.insert_one(ffSensor)
    gffSensor.set(ffAct)

    return ffAct

def sendData():
    humidity = dht22Humi()
    temp = dht22Temp()
    pm2_5in = PMin()
    pm2_5out = PMout()
    winActuation = windowActuation()
    ffActuation = filterfanActuation()
    timestamp = timeStamper()

    print("sends data")

    #logging info for prometheus
    log.info("Temp:{0:0.1f}*C, Humidity:{1:0.1f}%, PM2.5_in:{2:0.1f}μg/m3, PM2.5_out:{3:0.1f}μg/m3, windowActuation:{4:0.1f}, FilterfanActuation:{5:0.1f}, Time:{6:0.1f}".format(temp, humidity, pm2_5in, pm2_5out,winActuation, ffActuation, timestamp))

    #print
    print("Temp: ", temp, "Humidity: ", humidity, "PM2.5_in: ", pm2_5in, "PM2.5_out: ", pm2_5out, "windowActuation: ", winActuation, "FilterfanActuation: ", ffActuation, "Time: ", timestamp)

def idGenerator():
    newID = ObjectId(generate())
    #print(newID)
    return newID

def actUpdate():
    global winAct
    global ffAct

    cursorW = colWindow.find_one({}, sort=[('time', -1)])
    valueBeforeW = cursorW["value"]

    cursorF = colFilter.find_one({}, sort=[('time', -1)])
    valueBeforeF = cursorF["value"]

    if winAct != valueBeforeW:
        if cursorW == None:
            print("No data")
        else:
            id = cursorW["_id"]
            type = cursorW["type"]
            unit = cursorW["unit"]
            time = cursorW["time"]
            newIDW = idGenerator()

            colWindow.delete_one({"_id": id})
            colWindow.insert_one({"_id": newIDW, "value":winAct, "type":type, "unit":unit, "time":time})
            #print(id)
            #print(newID)
            cursor2W = colWindow.find_one({}, sort=[('time', -1)])

        print("before: ", valueBeforeW, "after: ", cursor2W["value"])
    else:
        print("No state change in window actuation")


    if ffAct != valueBeforeF:
        if cursorF == None:
            print("No data")
        else:
            id = cursorF["_id"]
            type = cursorF["type"]
            unit = cursorF["unit"]
            time = cursorF["time"]
            newIDF = idGenerator()

            colWindow.delete_one({"_id": id})
            colWindow.insert_one({"_id": newIDF, "value":ffAct, "type":type, "unit":unit, "time":time})
            #print(id)
            #print(newID)
            cursor2F = colWindow.find_one({}, sort=[('time', -1)])

        print("before: ", valueBeforeF, "after: ", cursor2F["value"])
    else:
        print("No state change in filterfan actuation")

    #sleep(1)


if __name__ == "__main__":
    metrics_port = 8000
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))

    #sleep(120)
    winAct = 0
    ffAct = 0
    PM2_5in = 53
    PM2_5out = 77

    readInterval = 10
    timeStart = time.time()
    actuateTime = 0
    sendData()

    rateIn = 5
    rateOut = 10
    getActuationData()

    while True:
        while time.time() < timeStart + readInterval:
            getActuationData()
            pm25indoor(rateIn)
            pm25outdoor(rateOut)
            print("pmIN: ", PM2_5in, "pmOUT: ", PM2_5out, "winAct: ", winAct, "ffAct: ", ffAct)
            
            if winAct == 1:
                #actuateTime = 0
                if PM2_5in >= 80:
                    if PM2_5out < 80:
                        ffAct = 0
                        print("window opened")
                        pm25indoor(-40)
                        actUpdate()
                    else:
                        winAct = 0
                        ffAct = 1
                        actUpdate()

                        #pm25indoor(-10)
                else:
                    winAct = 0
                    ffAct = 0
                    actUpdate()
            if ffAct == 1:
                #actuateTime = 0
                if PM2_5in >= 80:
                    if PM2_5out < 80:
                        ffAct = 0
                        winAct = 1
                        actUpdate()
                        #pm25indoor(-10)
                    else:
                        winAct = 0
                        print("ff opened")
                        pm25indoor(-50)
                        actUpdate()
                else:
                    winAct = 0
                    ffAct = 0
                    actUpdate()
            else:
                if PM2_5in >= 80:
                    print("pls actuate")
                    if actuateTime == 0:
                        actuateTime = time.time() + 5
                        print("here")
                    else:
                        if time.time() >= actuateTime:
                            print("forced actuation")
                            winAct = 1
                            ffAct = 1
                            actuateTime = 0
                            actUpdate()

            print("pmIN: ", PM2_5in, "pmOUT: ", PM2_5out, "winAct: ", winAct, "ffAct: ", ffAct)
        sendData()
        
        try:
            # Take timed input using inputimeout() function
            rateIn = inputimeout(prompt='Change rate Indoor:', timeout=3)
            rateIn = int(rateIn)
        
        except Exception as e:
            # Declare the timeout statement
            time_over = 'Indoor Rate not changed'
            print(time_over)
        
        try:
            rateOut = inputimeout(prompt='Change rate Outdoor:', timeout=3)
            rateOut = int(rateOut)

        except Exception as e:
            # Declare the timeout statement
            time_over = 'Outdoor Rate not changed'
            print(time_over)

        timeStart = time.time()
            