from prometheus_client import Gauge, start_http_server
from systemd.journal import JournalHandler

import logging 
import time
import random
import datetime
from inputimeout import inputimeout


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
db = client.HTTPSmartFarm
#dbActuate = client.HTTPSmartFarm_actuate
colHumi = db.dht22Humi
colTemp = db.dht22Temp
colpH = db.pHsensor
colWaterlevel = db.waterLevel
colECmeter = db.ECmeter
colmotorSensor = db.motorSensor
colflowMeter = db.flowMeter
coloverflowSensor = db.overflowSensor
colSolenoidValve = db.solenoidValve
colActuation = db.solenoidValve_actuate

# Setup logging to the Systemd Journal
log = logging.getLogger('dht22_sensor')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

#Gauges for humidity and temperature
gHumidity = Gauge('dht22_humidity', 'Humidity percentage measured by the DHT22 Sensor')
gTemperature = Gauge('dht22_temperature', 'Temperature measured by the DHT22 Sensor')
gpHvalue = Gauge('pH_sensor', 'pH level measured by the pH sensor')
gWaterLevel = Gauge('water_level_sensor', 'water level measured by the water level sensor')
gEC = Gauge('EC_meter', 'amount of nutrients measured by the electric conductivity sensor')
gSolenoidValve = Gauge('solenoid_valve', 'actuation for external source')
gmotorSensor = Gauge('motor_sensor', 'sensor for on and off status of water pump')
gflowMeter = Gauge('flow_meter', 'sensor to note wheter draining is complete')
goverflowSensor = Gauge('overflow_sensor', 'sensor to signal whether reservoir is full and overflowing')


def getActuationData():
    global actuation
    
    cursor = colActuation.find_one({}, sort=[('time', -1)])

    if cursor == None:
        actuation = 0
    else:
        actuation = cursor["value"]

    svUpdate()


def flood():
    global actuation
    global gallons
    global refillFlag
    global motorSensor
    global flowMeter
    global waterDrain

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

    if waterDrain >= 0.1078125:
        gallons = round((gallons + 0.1078125), 7) 
        waterDrain = round((waterDrain - 0.1078125 - leakage),7)
        if waterDrain < 0:
            waterDrain = 0
        flowMeter = 1
    else:
        flowMeter = 0
    
    sleep(47/64)

#def leakage(leak):
#   return leak

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
        gallons = gallons + 1
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
    humidity = random.randint(40,60)

    dht22SensorHumi = {
            "value":humidity,
            "type":"humidity",
            "unit":"%",
            "time":timeStamper()
            }
    
    colHumi.insert_one(dht22SensorHumi)
    gHumidity.set(humidity)

    return humidity

def dht22Temp   ():
    temperature = random.randint(20,24)

    dht22SensorTemp = {
            "value":temperature,
            "type":"temperature",
            "unit":"°C",
            "time":timeStamper()
            }
    
    colTemp.insert_one(dht22SensorTemp)
    gTemperature.set(temperature)

    return temperature

def pHsensor():
    pHvalue = round(random.uniform(5.8,6.3),2)

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
            "unit":"µmhos/cm",
            "time":timeStamper()
            }
    
    colECmeter.insert_one(ECSensor)
    gEC.set(EC)

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
    gWaterLevel.set(gallons)

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
    humidity = dht22Humi()
    temp = dht22Temp()
    pH = pHsensor()
    EC = ECmeter()
    waterLevel = waterLevel_sensor()
    waterPump = motor()
    drainIndicator = flow()
    overflowIndicator = overflow()
    solValve = solenoidValve()
    timeStamp = timeStamper()

    #logging
    log.info("Temp:{0:0.1f}*C, Humidity:{1:0.1f}%, pHvalue:{2:0.1f}, WaterLevel:{3:0.1f}, EC:{4:0.1f}, waterPump:{5:0.1f},  flowMeter{6:0.1f}, overflowSensor{7:0.1f}, Actuation:{8:0.1f}, Time:{9:0.1f}".format(temp, humidity, pH, waterLevel, EC, waterPump, drainIndicator, overflowIndicator, solValve, timeStamp))

    #printing
    print('humidity:',humidity, 'temp:',temp,'pHvalue:', pH, 'waterLevel:', waterLevel, 'EC:', EC, 'waterPump:', waterPump, 'flowMeter:', drainIndicator, 'overflowSensor:', overflowIndicator, 'actuationStatus:', solValve,'timeStamp:', timeStamp)

def svUpdate():
    global actuation

    cursor = colSolenoidValve.find_one({}, sort=[('time', -1)])
    valueBefore = cursor["value"]

    if cursor == None:
        print("No data")
    else:
        id = cursor["_id"]
        colSolenoidValve.update_one({"_id": id}, {"$set": {"value": actuation}})
        print(id)
        cursor2 = colSolenoidValve.find_one({}, sort=[('time', -1)])
    print("before: ", valueBefore, "after: ", cursor2["value"])

if __name__ == "__main__":
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

    #cursor = colSolenoidValve.find_one({}, sort=[('time', -1)])

    #if cursor == None:
    #    actuation = 0
    #else:
    #    id = cursor["_id"]

    #colSolenoidValve.update_one({"_id": id}, {"$set": {"value": 1}})
    #print(id)

    while True:
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
                flood()
            drain(leakage)
            #print(actuation, gallons, waterDrain)
            print('actuation:', actuation, 'waterLevel:', gallons, 'watertoDrain:', waterDrain)
        sendData()
        try:
            leakage = inputimeout(prompt='leakage:', timeout=3)
            leakage = int(leakage)
        except Exception as e:
            time_over = 'Leakage not changed'
            print(time_over)

        timeStart = time.time()