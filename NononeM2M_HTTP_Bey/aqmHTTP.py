#for prometheus and logging
from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler
import logging 

#for system reference
import time
import random
import datetime
from inputimeout import inputimeout
from random_object_id import generate
from bson import ObjectId

#for mongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#mongoDB connection string to nonOneM2M project
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
colHumiIN = db.dht22Humi_indoor
colHumiOUT = db.dht22Humi_outdoor
colTempIN = db.dht22Temp_indoor
colTempOUT = db.dht22Temp_outdoor
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
gHumidityIN = Gauge('dht22_humidity_indoor', 'Humidity percentage measured by the DHT22 Sensor indoor')
gHumidityOUT = Gauge('dht22_humidity_outdoor', 'Humidity percentage measured by the DHT22 Sensor outdoor')
gTemperatureIN = Gauge('dht22_temperature_indoor', 'Temperature measured by the DHT22 Sensor indoor')
gTemperatureOUT = Gauge('dht22_temperature_outdoor', 'Temperature measured by the DHT22 Sensor outdoor')
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

def dht22HumiIN():
    humidityIN = random.randint(72,87)

    dht22SensorHumi = {
            "value":humidityIN,
            "type":"humidity",
            "unit":"%",
            "time":timeStamper()
            }
    
    colHumiIN.insert_one(dht22SensorHumi)
    gHumidityIN.set(humidityIN)

    return humidityIN

def dht22HumiOUT():
    humidityOUT = random.randint(72,87)

    dht22SensorHumi = {
            "value":humidityOUT,
            "type":"humidity",
            "unit":"%",
            "time":timeStamper()
            }
    
    colHumiOUT.insert_one(dht22SensorHumi)
    gHumidityOUT.set(humidityOUT)

    return humidityOUT

def dht22TempIN():
    temperatureIN = random.randint(25,31)

    dht22SensorTemp = {
            "value":temperatureIN,
            "type":"temperature",
            "unit":"°C",
            "time":timeStamper()
            }
    
    colTempIN.insert_one(dht22SensorTemp)
    gTemperatureIN.set(temperatureIN)

    return temperatureIN

def dht22TempOUT():
    temperatureOUT = random.randint(25,31)

    dht22SensorTemp = {
            "value":temperatureOUT,
            "type":"temperature",
            "unit":"°C",
            "time":timeStamper()
            }
    
    colTempOUT.insert_one(dht22SensorTemp)
    gTemperatureOUT.set(temperatureOUT)

    return temperatureOUT

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
    pm2_5in = PMin()
    sleep(1)
    print("PM2.5_IN:", pm2_5in)
    humidityIN = dht22HumiIN()
    sleep(1)
    pm2_5out = PMout()
    sleep(1)
    print("PM2.5_OUT:", pm2_5out)
    humidityOUT = dht22HumiOUT()
    sleep(1)
    winActuation = windowActuation()
    sleep(1)
    print("winAct:", winActuation)
    tempIN = dht22TempIN()
    sleep(1)
    ffActuation = filterfanActuation()
    sleep(1)
    print("ffAct:", ffActuation)
    tempOUT = dht22TempOUT()
    sleep(1)
    timestamp = timeStamper()
    sleep(1)

    print("sends data")

    #logging info for prometheus
    log.info("Temp_IN:{0:0.1f}*C, Temp_OUT:{1:0.1f}*C, Humidity_IN:{2:0.1f}%, Humidity_OUT:{3:0.1f}%, PM2.5_in:{4:0.1f}μg/m3, PM2.5_out:{5:0.1f}μg/m3, windowActuation:{6:0.1f}, FilterfanActuation:{7:0.1f}, Time:{8:0.1f}".format(tempIN, tempOUT, humidityIN, humidityOUT, pm2_5in, pm2_5out,winActuation, ffActuation, timestamp))

    #print
    print("Temp_IN: ", tempIN, "Temp_OUT: ", tempOUT, "Humidity_IN: ", humidityIN, "Humidity_OUT: ", humidityOUT, "PM2.5_in: ", pm2_5in, "PM2.5_out: ", pm2_5out, "windowActuation: ", winActuation, "FilterfanActuation: ", ffActuation, "Time: ", timestamp)

def idGenerator():
    newID = ObjectId(generate())
    #print(newID)
    return newID

def actUpdate():
    global winAct
    global ffAct

    cursorW = colWindow.find_one({}, sort=[('time', -1)])
    

    cursorF = colFilter.find_one({}, sort=[('time', -1)])
    

    if cursorW != None:
        valueBeforeW = cursorW["value"]
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

    if cursorF != None:
        valueBeforeF = cursorF["value"]
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

    readInterval = 5
    timeStart = time.time()
    actuateTime = 0
    sendData()

    rateIn = 3
    rateOut = 5
    getActuationData()

    numberData = 0

    while numberData != 100:
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

        numberData = numberData + 1
        timeStart = time.time()
            