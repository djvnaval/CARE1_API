# notes:
# Smart Farm Monitoring System
# IPE - Sensors and actuators
# using MQTT protocol


from random import random
from datetime import datetime

from openmtc_app.onem2m import XAE
from openmtc_onem2m.model import Container

import pymongo
import time

MONGO_URI = 'mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority'


class IPE(XAE):
    remove_registration = True

    # sensors to create
    sensors = [
        'Humi',                     
        'Temp',
        'pH',
        'WaterLevel',
        'ElecConductivity',
        'MotorSensor',
        'OverflowSensor',           
        'FlowMeter' 
    ]

    actuators = [
        'SolenoidValve'
    ]

    # settings for random sensor data generation
    # offset = minimum value
    # range = max - min

    # Humidity: 40% to 70%
    humi_range = 30
    humi_offset = 40
    
    # Temperature: 20degC to 30degC
    temp_range = 10
    temp_offset = 20

    # pH value: 5.5 to 7.5
    pH_range = 20
    pH_offset = 55     # to be divided by 10 later in getting the value

    # Electric Conductivity: 1 to 2.5
    ec_range = 15
    ec_offset = 10     # to be divided by 10 later in getting the value

    # Water Level in the tank
    water_level = 50    # tank capacity
    water_drain = 0

    # Motor Sensor: status of water pump
    motor_ON = 1        # water is pumping
    motor_OFF = 0       # water is not pumping

    motor = motor_OFF 

    # Overflow Sensor: is reservoir full and overflowing
    overflow_ON = 1     # tank is full
    overflow_OFF = 0    # tank is not yet full

    overflow = overflow_OFF

    # Flow Meter: is draining complete
    flow_ON = 1         # it is draining
    flow_OFF = 0        # draining complete

    flow = flow_OFF

    # Actuator: solenoid valve
    valve_ON = 1        # refilling water throughout the smart farm
    valve_OFF = 0       # stop refilling

    actuation = valve_OFF
    refill_flag = 0

    def _on_register(self):

        # init variables
        self._recognized_sensors = {}
        self._recognized_measurement_containers = {}
        self._command_containers = {}

        # init base structure
        label = 'devices_mqtt'
        container = Container(resourceName=label)
        self._devices_container = self.create_container(None,
                                                        container,
                                                        labels=[label],
                                                        max_nr_of_instances=0)
        
        # create container for each actuator
        for actuator in self.actuators:
            actuator_container = Container(resourceName=actuator)
            self.create_container(
                self._devices_container.path,  # the target resource/path parenting the Container
                actuator_container,            # the Container resource or a valid container ID
                max_nr_of_instances=0,         # the container's max_nr_of_instances (here: 0=unlimited)
                labels=['actuator']            # (optional) the container's labels
            )
            # create container for the commands of the actuators
            commands_container = Container(resourceName='commands')
            commands_container = self.create_container(
                actuator_container.path,
                commands_container,
                max_nr_of_instances=3,
                labels=['commands']
            )
            # add commands_container of current actuator to self._command_containers
            self._command_containers[actuator] = commands_container
            # subscribe to command container of each actuator to the handler command
            
            self.add_container_subscription(
                commands_container.path,    # the Container or it's path to be subscribed
                self.handle_command         # reference of the notification handling function
            )

        # trigger periodically new data generation
        # every seconds
        self.run_forever(5, self.smartfarm_system)

        # log message
        self.logger.debug('registered')

    def handle_command(self, container, content):
        print('handle_valve...')
        print('container: %s' % container)
        print('value: %s' % content)
        print('')

    def get_actuation_data(self):
        
        cursor = col_actuation.find_one({}, sort=[('time', -1)])

        if cursor == None:
            actuation = self.valve_OFF
        else:
            actuation = self.valve_ON if cursor["value"] == 1 else self.valve_OFF

        return actuation
    
    def smartfarm_system(self):
        # the flowchart

        self.get_sensor_data()

        print('\n%s: actuation: %s, water level: %s gallons, water to drain: %s gallons' 
              % (datetime.now(), 'valveOFF' if self.actuation==0 else 'valveON', self.water_level, self.water_drain))

        self.actuation = self.get_actuation_data()
        self.push_actuator_data(self.actuation)

        if self.actuation == 1:
            self.refill()
            
        self.flood()
        print('%s: actuation: %s, water level: %s gallons, water to drain: %s gallons' 
              % (datetime.now(), 'valveOFF' if self.actuation==0 else 'valveON', self.water_level, self.water_drain))

        if self.refill_flag == 1:
            actuate_time = time.time() + 5

            while self.actuation != self.valve_ON:
                self.actuation = self.get_actuation_data()
                self.push_actuator_data(self.actuation)
                print("PLEASE ACTUATE...")

                if time.time() >= actuate_time:
                    self.actuation = self.valve_ON
                    self.push_actuator_data(self.actuation)
                    
            
            self.refill_flag = 0
            
            print('%s: actuation: %s, water level: %s gallons, water to drain: %s gallons' 
              % (datetime.now(), 'valveOFF' if self.actuation==0 else 'valveON', self.water_level, self.water_drain))
            self.push_actuator_data(self.actuation)

            self.refill()
            self.flood()

        self.drain()
        print('%s: actuation: %s, water level: %s gallons, water to drain: %s gallons\n' 
              % (datetime.now(), 'valveOFF' if self.actuation==0 else 'valveON', self.water_level, self.water_drain))
        self.push_actuator_data(self.actuation)



    def get_sensor_data(self):

        for name in self.sensors:
            if name.startswith('Humi'):
                value = self.humi_random_data()
            elif name.startswith('Temp'):
                value = self.temp_random_data()
            elif name.startswith('pH'):
                value = self.ph_random_data()
            elif name.startswith('WaterLevel'):
                value = self.water_level
            elif name.startswith('ElecConductivity'):
                value = self.ec_random_data()
            elif name.startswith('MotorSensor'):
                value = self.motor
            elif name.startswith('OverflowSensor'):
                value = self.overflow
            elif name.startswith('FlowMeter'):
                value = self.flow
            else:
                continue

            current_date_time = str(datetime.now())

            self.handle_sensor_data(name, value, current_date_time)

    def push_actuator_data(self, value):
        data = {
            "value" : value,
			"type" : "solenoid valve",
			"unit" : "",
			"time" : str(datetime.now())
        }

        print ("Solenoid valve: %s" % (data))

        self.push_content(self._command_containers['SolenoidValve'], data)
        
            
    def humi_random_data(self):
        return int(random() * self.humi_range + self.humi_offset)
    
    def temp_random_data(self):
        return int(random() * self.temp_range + self.temp_offset)
    
    def ph_random_data(self):
        return int(random() * self.pH_range + self.pH_offset)/10
    
    def ec_random_data(self):
        return int(random() * self.ec_range + self.ec_offset)/10

    def handle_sensor_data(self, sensor, value, time):

        # initialize sensor structure if never done before
        if sensor not in self._recognized_sensors:
            self.create_sensor_structure(sensor)
        self.push_sensor_data(sensor, value, time)

    def create_sensor_structure(self, sensor):
        print('initializing sensor: %s' % sensor)

        # create sensor container
        device_container = Container(resourceName=sensor)
        device_container = self.create_container(self._devices_container.path,
                                                 device_container,
                                                 labels=['sensor'],
                                                 max_nr_of_instances=0)

        
        # add sensor to _recognized_sensors
        self._recognized_sensors[sensor] = device_container
        

        # create measurements container
        labels = ['measurements']
        if sensor.startswith('Humi'):
            labels.append('humidity')
        elif sensor.startswith('Temp'):
            labels.append('temperature')
        elif sensor.startswith('pH'):
            labels.append('pH value')
        elif sensor.startswith('WaterLevel'):
            labels.append('water level')
        elif sensor.startswith('ElecConductivity'):
            labels.append('electric conductivity')
        elif sensor.startswith('MotorSensor'):
            labels.append('motor sensor')
        elif sensor.startswith('OverflowSensor'):
            labels.append('overflow sensor')
        elif sensor.startswith('FlowMeter'):
            labels.append('flow meter sensor')
        else:
            pass

        measurements_container = Container(resourceName='measurements')
        measurements_container = self.create_container(device_container.path,
                                                       measurements_container,
                                                       labels=labels,
                                                       max_nr_of_instances=3)

        # add measurements_container from sensor to _recognized_measurement_containers
        self._recognized_measurement_containers[sensor] = measurements_container

    def push_sensor_data(self, sensor, value, time):

        # build data set with value and metadata
        if sensor.startswith('Humi'):
            data = {
                'value': value,
                'type': 'humidity',
                'unit': 'percentage',
                'time': time
            }
        elif sensor.startswith('Temp'):
            data = {
                'value': value,
                'type': 'temperature',
                'unit': 'degreeC',
                'time': time
            }
        elif sensor.startswith('pH'):
            data = {
                'value': value,
                'type': 'pH value',
                'unit': '',
                'time': time
            }
        elif sensor.startswith('WaterLevel'):
            data = {
                'value': value,
                'type': 'water level',
                'unit': 'gallons',
                'time': time
            }
        elif sensor.startswith('ElecConductivity'):
            data = {
                'value': value,
                'type': 'electric conductivity',
                'unit': 'mS/cm',
                'time': time
            }
        elif sensor.startswith('MotorSensor'):
            data = {
                'value': value,
                'type': 'motor sensor',
                'unit': '',
                'time': time
            }
        elif sensor.startswith('OverflowSensor'):
            data = {
                'value': value,
                'type': 'overflow sensor',
                'unit': '',
                'time': time
            }
        elif sensor.startswith('FlowMeter'):
            data = {
                'value': value,
                'type': 'flow meter sensor',
                'unit': '',
                'time': time
            }
        else:
            data = {
                'value': 0,
                'type': '',
                'unit': '',
                'time': time
            }

        # print the new data set
        print ("%s: %s" % (sensor, data))

        # finally, push the data set to measurements_container of the sensor
        self.push_content(self._recognized_measurement_containers[sensor], data)

    def refill(self):
        self.motor = self.motor_OFF

        if self.flow == self.flow_OFF and self.water_level < 50 and self.actuation == self.valve_ON:
            self.water_level += 1
            self.overflow = self.overflow_OFF

        if self.water_level > 60:
            self.overflow = self.overflow_ON
            self.actuation = self.valve_OFF
        else:
            self.overflow = self.overflow_OFF
            self.actuation = self.valve_OFF
        self.push_actuator_data(self.actuation)

    def drain(self):
        self.motor = self.motor_OFF

        if self.water_drain >= 0.1078125:
            self.water_level = round((self.water_level + 0.1078125), 7) 
            self.water_drain = round((self.water_drain - 0.1078125), 7)
            if self.water_drain < 0:
                self.water_drain = 0
            self.flow = self.flow_ON

        else:
            self.flow = self.flow_OFF

        time.sleep(47/64)
        self.push_actuator_data(self.actuation)

    def flood(self):
        if self.flow == self.flow_OFF:
            remaining_water = self.water_level - 26

            if remaining_water >= 0:
                self.actuation = self.valve_OFF

                while (self.water_level != remaining_water):
                    self.water_level -= 1
                    self.motor = self.motor_ON

                self.water_drain = 25.875
                self.refill_flag = 0
            
            else:
                print("Message: Not enough nutrient solution.")
                self.motor = self.motor_OFF
                self.refill_flag = 1
        self.push_actuator_data(self.actuation)
    


if __name__ == "__main__":

    from openmtc_app.runner import AppRunner as Runner

    # Setup MongoDB connection
    mongo_client = pymongo.MongoClient(MONGO_URI)

    db = mongo_client.oneM2M_MQTT_SmartFarm
    col_actuation = db.solenoidValve_actuate

    host = "mqtts://upCARE1_onem2m:updilimanCARE1@29c49bdf585f4e6d8e93e1522dc5e23f.s1.eu.hivemq.cloud:8883#mn-cse-1"
    app = IPE(
        # SSL options
        name = 'MQTT_SmartFarm',
        originator_pre='//openmtc.org/mn-cse-1',  # originator_pre, needs to match value in cert
        ca_certs='../../openmtc-gevent/certs/ca-chain.cert.pem',
        cert_file='certs/test-ipe.cert.pem',      # cert file, pre-shipped and should match name
        key_file='certs/test-ipe.key.pem'
    )
    Runner(app).run(host)
