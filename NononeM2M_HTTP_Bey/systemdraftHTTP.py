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

#Connection String to mongoDB project
uri = "mongodb+srv://HTTPSystem:HTTPnonOneM2M@nononem2m.lold0yl.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Database
db = client.HTTPSmartFarm

#collections for sensor and actuator data
colHumi = db.dht22Humi
colTemp = db.dht22Temp
colpH = db.pHsensor
colWaterlevel = db.waterLevel
colECmeter = db.ECmeter
colmotorSensor = db.motorSensor
colflowMeter = db.flowMeter
coloverflowSensor = db.overflowSensor
colSolenoidValve = db.solenoidValve

#collection for actuation commands
colActuation = db.solenoidValve_actuate

# Setup logging to the Systemd Journal
log = logging.getLogger('dht22_sensor')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

#Gauges for Sensor and Actuator IPEs
gHumidity = Gauge('dht22_humidity', 'Humidity percentage measured by the DHT22 Sensor', ['scale'])
gTemperature = Gauge('dht22_temperature', 'Temperature measured by the DHT22 Sensor', ['scale'])
gpHvalue = Gauge('pH_sensor', 'pH level measured by the pH sensor')
gWaterLevel = Gauge('water_level_sensor', 'water level measured by the water level sensor', ['scale'])
gEC = Gauge('EC_meter', 'amount of nutrients measured by the electric conductivity sensor', ['scale'])
gSolenoidValve = Gauge('solenoid_valve', 'actuation for external source')
gmotorSensor = Gauge('motor_sensor', 'sensor for on and off status of water pump')
gflowMeter = Gauge('flow_meter', 'sensor to note wheter draining is complete')
goverflowSensor = Gauge('overflow_sensor', 'sensor to signal whether reservoir is full and overflowing')


def getActuationData():
    global actuation
    
    cursor = colActuation.find().sort('time', -1).limit(1)
    #print(type(cursor))

    #cursor = colActuation.find_one({}, sort=[('time', -1)])
    if cursor == None:
        actuation = 0
    else:
        actuation = cursor[0]["value"]
    #print(cursor[0]["_id"])
    svUpdate()


def flood():
    global actuation
    global gallons
    global refillFlag
    global motorSensor
    global flowMeter
    global waterDrain
    global overflowSensor

    overflowSensor = 0

    #if gallons == (gallons - idealLoss(instance, set)):
    if flowMeter == 0:
        remainingGallon = gallons - 26
        if (remainingGallon) >= 0:
            actuation = 0
            while gallons != (remainingGallon):
                gallons = gallons - 1
                motorSensor = 1
                #moistureSensor = 1
            waterDrain = 25.875
            refillFlag = 0
        else:
            print("not enough nutrient solution")
            motorSensor = 0
            refillFlag = 1
    svUpdate()

def drain(leakage):
    global motorSensor
    global flowMeter
    global gallons
    global waterDrain

    motorSensor = 0

    if waterDrain >= 1.078125:
        gallons = round((gallons + 1.078125), 7) 
        waterDrain = round((waterDrain - 1.078125 - leakage),7)
        if waterDrain < 0:
            waterDrain = 0
        flowMeter = 1
    else:
        flowMeter = 0
        waterDrain = 0
    
    #sleep(47/64)


def sleep(seconds):
    time.sleep(seconds)

def refill():
    global gallons
    global overflowSensor
    global actuation
    global waterDrain
    global motorSensor
    global flowMeter

    motorSensor = 0

    if flowMeter == 0 and gallons < 50 and actuation == 1:
        gallons = gallons + 3
        overflowSensor = 0

    if gallons > 60:
        overflowSensor = 1
        actuation = 0
    else:
        overflowSensor = 0
        actuation = 0
    
    svUpdate()
    
def timeStamper():
    timeStamp = datetime.datetime.now()
    return timeStamp


def dht22Humi():
    humidity = random.randint(30,50)

    dht22SensorHumi = {
            "value":humidity,
            "type":"humidity",
            "unit":"%",
            "time":timeStamper()
            }
    
    colHumi.insert_one(dht22SensorHumi)
    gHumidity.labels('%').set(humidity)

    return humidity

def dht22Temp   ():
    temperature = random.randint(34,38)

    dht22SensorTemp = {
            "value":temperature,
            "type":"temperature",
            "unit":"°C",
            "time":timeStamper()
            }
    
    colTemp.insert_one(dht22SensorTemp)
    gTemperature.labels('°C').set(temperature)

    return temperature

def pHsensor():
    pHvalue = round(random.uniform(5.5,6),2)

    pHSensor = {
            "value":pHvalue,
            "type":"pH value",
            "unit":"none",
            "time":timeStamper()
            }
    
    colpH.insert_one(pHSensor)
    gpHvalue.set(pHvalue)

    return pHvalue

def ECmeter():
    EC = round(random.uniform(1,2.5),2)

    ECSensor = {
            "value":EC,
            "type":"electric conductivity",
            "unit":"mS/cm",
            "time":timeStamper()
            }
    
    colECmeter.insert_one(ECSensor)
    gEC.labels('mS/cm').set(EC)

    return EC

def waterLevel_sensor():
    #print("water sensor upload")
    global gallons 

    waterlevelSensor = {
            "value":gallons,
            "type":"water level",
            "unit":"gallons",
            "time":timeStamper()
            }
    
    colWaterlevel.insert_one(waterlevelSensor)
    gWaterLevel.labels('gallons').set(gallons)

    return gallons

def solenoidValve():
    global actuation 

    getActuationData()
    
    solenoidValve = {
            "value":actuation,
            "type":"solenoid valve",
            "unit":"none",
            "time":timeStamper()
            }
    
    colSolenoidValve.insert_one(solenoidValve)
    gSolenoidValve.set(actuation)

    return actuation

def flow():
    global flowMeter

    flow = {
        "value":flowMeter,
        "type":"flow meter",
        "unit":"none",
        "time":timeStamper()
    }

    colflowMeter.insert_one(flow)
    gflowMeter.set(flowMeter)

    return flowMeter

def motor():
    global motorSensor

    motor = {
        "value":motorSensor,
        "type":"motor sensor",
        "unit":"none",
        "time":timeStamper()
    }

    colmotorSensor.insert_one(motor)
    gmotorSensor.set(motorSensor)

    return motorSensor

def overflow():
    global overflowSensor

    overflow = {
        "value":overflowSensor,
        "type":"overflow sensor",
        "unit":"none",
        "time":timeStamper()
    }

    coloverflowSensor.insert_one(overflow)
    goverflowSensor.set(overflowSensor)

    return overflowSensor


def sendData():
    print("sends Data")
    waterLevel = waterLevel_sensor()
    print("waterLevel: ", waterLevel)
    sleep(1)
    humidity = dht22Humi()
    sleep(1)
    temp = dht22Temp()
    sleep(1)
    solValve = solenoidValve()
    print("solValve: ", solValve)
    sleep(1)
    pH = pHsensor()
    sleep(1)
    EC = ECmeter()
    sleep(1)
    waterPump = motor()
    sleep(1)
    drainIndicator = flow()
    sleep(1)
    overflowIndicator = overflow()
    sleep(1)
    timeStamp = timeStamper()
    sleep(1)

    #logging
    log.info("Temp:{0:0.1f}*C, Humidity:{1:0.1f}%, pHvalue:{2:0.1f}, WaterLevel:{3:0.1f}, EC:{4:0.1f}, waterPump:{5:0.1f},  flowMeter{6:0.1f}, overflowSensor{7:0.1f}, Actuation:{8:0.1f}, Time:{9:0.1f}".format(temp, humidity, pH, waterLevel, EC, waterPump, drainIndicator, overflowIndicator, solValve, timeStamp))

    #printing
    print('humidity:',humidity, 'temp:',temp,'pHvalue:', pH, 'waterLevel:', waterLevel, 'EC:', EC, 'waterPump:', waterPump, 'flowMeter:', drainIndicator, 'overflowSensor:', overflowIndicator, 'actuationStatus:', solValve,'timeStamp:', timeStamp)


def idGenerator():
    newID = ObjectId(generate())
    #print(newID)
    return newID

def svUpdate():
    global actuation

    cursor = colSolenoidValve.find_one({}, sort=[('time', -1)])
    if cursor != None:
        valueBefore = cursor["value"]

        if actuation != valueBefore:
            if cursor == None:
                print("No data")
            else:
                id = cursor["_id"]
                type = cursor["type"]
                unit = cursor["unit"]
                time = cursor["time"]
                newID = idGenerator()

                colSolenoidValve.delete_one({"_id": id})
                colSolenoidValve.insert_one({"_id": newID, "value":actuation, "type":type, "unit":unit, "time":time})
                #print(id)
                #print(newID)
                cursor2 = colSolenoidValve.find_one({}, sort=[('time', -1)])

            print("before: ", valueBefore, "after: ", cursor2["value"])
        else:
            print("no change in actuation state")
    
    #sleep(1)

if __name__ == "__main__":
    
    #start http connection
    metrics_port = 8001
    start_http_server(metrics_port)
    print("Serving sensor metrics on :{}".format(metrics_port))
    log.info("Serving sensor metrics on :{}".format(metrics_port))
    
    actuation = 0
    getActuationData()
    gallons = 50
    waterDrain = 0
    flowMeter = 0
    motorSensor = 0
    overflowSensor = 0
    refillFlag = 0
    leakage = 0

    readInterval = 10
    timeStart = time.time()
    sendData()


    numberData = 0
    while numberData != 100:
        while time.time() < timeStart + readInterval:
            #print(actuation, gallons, waterDrain)
            getActuationData()
            #print(actuation, gallons, waterDrain)
            print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
            if actuation == 1:
                refill()
            flood()
            #print(actuation, gallons, waterDrain)
            print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
            if refillFlag == 1:
                actuateTime = time.time() + 5
                while actuation != 1:
                    getActuationData()
                    print("please actuate")
                    if time.time() >= actuateTime:
                        actuation = 1 
                        svUpdate()
                refillFlag = 0
                print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
                refill()
                print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
                flood()
                print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
            drain(leakage)
            print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
            #print(actuation, gallons, waterDrain)
            print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
        sendData()
        
        try:
            leakage = inputimeout(prompt='leakage:', timeout=3)
            leakage = int(leakage)
        except Exception as e:
            time_over = 'Leakage not changed'
            print(time_over)

        numberData = numberData + 1
        timeStart = time.time()