# notes:
# Air Quality Monitoring System
# IPE - Sensors and actuators
# using MQTT protocol


from random import random, randint
from datetime import datetime

from openmtc_app.onem2m import XAE
from openmtc_onem2m.model import Container
from pymongo import MongoClient
from random_object_id import generate
from bson import ObjectId
from inputimeout import inputimeout

import time


class IPE(XAE):
    remove_registration = True

    # sensors to create
    sensors = [
        'Humi_in',
        'Humi_out',
        'Temp_in',
        'Temp_out',
        'PM2_5_in',
        'PM2_5_out'
    ]

    actuators = [
        'Window',
        'FilterFan'
    ]

    # settings for random sensor data generation
    # offset = minimum value
    # range = max - min

    # Humidity: 60% to 90%
    humi_range = 30
    humi_offset = 60

    # Temperature: 25degC to 40degC
    temp_range = 15
    temp_offset = 25

    # PM 2.5: starting value
    pm25_in =53
    pm25_out = 77

    rate_in = 5
    rate_out = 10

    # Window Actuator
    window_OPEN = 1
    window_CLOSE = 0

    window_actuation = window_CLOSE

    # Filter Fan Actuator
    fan_ON = 1
    fan_OFF = 0

    fan_actuation = fan_OFF


    def _on_register(self):

        self.client = MongoClient('mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client["oneM2M_HTTP_AQM"]
        self.window_col = self.db.windowSensor_actuate
        self.fan_col = self.db.filterFanSensor_actuate

        # init variables
        self._recognized_sensors = {}
        self._recognized_measurement_containers = {}
        self._command_containers = {}

        # init base structure
        label = 'devices_http'
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

        self.windowCol = self.db["Window"]
        self.fanCol = self.db["FilterFan"]

        self.offset_start()

        # trigger periodically new data generation
        # in Hz
        self.run_forever(0.2, self.aqm_system)

        # log message
        self.logger.debug('registered')
    
    def offset_start(self):
        for name in self.sensors:
            if name.startswith('Humi'):
                value = self.humi_random_data()
            elif name.startswith('Temp'):
                value = self.temp_random_data()
            elif name.startswith('PM2_5_in'):
                value = self.pm2_5_in_data()
            elif name.startswith('PM2_5_out'):
                value = self.pm2_5_out_data()
            else:
                continue
            
            current_date_time = datetime.now()

            self.handle_sensor_data(name, value, current_date_time)

            time.sleep(randint(5,20))

    def handle_command(self, container, content):
        print('handle_valve...')
        print('container: %s' % container)
        print('value: %s' % content)
        print('')

    def get_window_data(self):

        window_cursor = self.window_col.find_one({}, sort=[('time', -1)])

        if window_cursor == None:
            self.window_actuation = self.window_CLOSE
        else:
            self.window_actuation = window_cursor["value"]

        self.window_update()

    def get_fan_data(self):

        fan_cursor = self.fan_col.find_one({}, sort=[('time', -1)])

        if fan_cursor == None:
            self.fan_actuation = self.fan_OFF
        else:
            self.fan_actuation = fan_cursor["value"]

        self.fan_update()

    def change_rate(self, timeover):
        try:
            self.rate_in = int(inputimeout(prompt="\nChange PM2.5 rate indoor: ", timeout=timeover))
        except:
            print("\nIndoor PM2.5 rate not changed.\n")
            self.rate_in = 5

        try:
            self.rate_out = int(inputimeout(prompt="\nChange PM2.5 rate outdoor: ", timeout=timeover))
        except:
            print("\nOutdoor PM2.5 rate not changed.\n")

    def aqm_system(self):
        self.get_sensor_data()
        self.get_window_data()
        self.get_fan_data()

        self.push_window_data(self.window_actuation)
        self.push_fan_data(self.fan_actuation)

        #self.rate_in = 5
        self.change_rate(4)

        self.get_sensor_data()

        if self.pm25_in >= 80:
            if self.pm25_out >= 80:
                if self.window_actuation == self.window_OPEN:
                    print("\nPLEASE ACTUATE: Close the window\n")
                    time.sleep(5)
                    self.get_window_data()

                    if self.window_actuation == self.window_OPEN:
                        self.window_actuation = self.window_CLOSE
                        print("\Forced actuation: Window closed!\n")
                        
                    self.push_window_data(self.window_actuation)
                    self.window_update()

                if self.fan_actuation == self.fan_OFF:
                    print("\nPLEASE ACTUATE: Turn on the filter fan\n")
                    time.sleep(5)
                    self.get_fan_data()

                    if self.fan_actuation == self.fan_OFF:
                        self.fan_actuation = self.fan_ON
                        print("\nForced actuation: Filter fan turned on!\n")
                    
                    self.push_fan_data(self.fan_actuation)
                    self.fan_update()

                self.rate_in = -50
                self.pm2_5_in_data()

            else:
                if self.window_actuation == self.window_CLOSE:
                    print("\nPLEASE ACTUATE: Open the window\n")
                    time.sleep(5)
                    self.get_window_data()

                    if self.window_actuation == self.window_CLOSE:
                        self.window_actuation = self.window_OPEN
                        print("\nForced actuation: Window opened!\n")
                    
                    self.push_window_data(self.window_actuation)
                    self.window_update()
                
                if self.fan_actuation == self.fan_ON:
                    print("\nPLEASE ACTUATE: Turn off the filter fan\n")
                    time.sleep(5)
                    self.get_fan_data()

                    if self.fan_actuation == self.fan_ON:
                        self.fan_actuation = self.fan_OFF
                        print("\nForced actuation: Filter fan turned off!\n")
                    
                    self.push_fan_data(self.fan_actuation)
                    self.fan_update()

                self.rate_in = -40
                self.pm2_5_in_data()

        else:
            if self.window_actuation == self.window_OPEN:
                print("\nPLEASE ACTUATE: Close the window\n")
                time.sleep(5)
                self.get_window_data()

                if self.window_actuation == self.window_OPEN:
                    self.window_actuation = self.window_CLOSE
                    print("\nForced actuation: Window closed!\n")
                
                self.push_window_data(self.window_actuation)
                self.window_update()

            if self.fan_actuation == self.fan_ON:
                print("\nPLEASE ACTUATE: Turn off the filter fan\n")
                time.sleep(5)
                self.get_fan_data()
                
                if self.fan_actuation == self.fan_ON:
                    self.fan_actuation = self.fan_OFF
                    print("\nForced actuation: Filter fan turned off!\n")
                
                self.push_fan_data(self.fan_actuation)
                self.fan_update()

        # just making sure that PM2.5 outdoor value is not always increasing
        if self.pm25_out >= 200:
            self.rate_out = -10
        elif self.pm25_out <= 40:
            self.rate_out = 10

    def get_sensor_data(self):

        for name in self.sensors:
            if name.startswith('Humi'):
                value = self.humi_random_data()
            elif name.startswith('Temp'):
                value = self.temp_random_data()
            elif name.startswith('PM2_5_in'):
                value = self.pm2_5_in_data()
            elif name.startswith('PM2_5_out'):
                value = self.pm2_5_out_data()
            else:
                continue
            
            current_date_time = datetime.now()

            self.handle_sensor_data(name, value, current_date_time)

            time.sleep(3)

    def humi_random_data(self):
        return int(random() * self.humi_range + self.humi_offset)
    
    def temp_random_data(self):
        return int(random() * self.temp_range + self.temp_offset)

    def pm2_5_in_data(self):
        self.pm25_in += self.rate_in
        return self.pm25_in

    def pm2_5_out_data(self):
        self.pm25_out += self.rate_out
        return self.pm25_out

    def push_window_data(self, value):
        data = {
            "value" : value,
			"type" : "window",
			"unit" : "",
			"time" : datetime.now()
        }

        self.windowCol.insert_one(data.copy())

        print("Window: %s" % (data))
        data['time'] = str(data['time'])

        self.push_content(self._command_containers['Window'], data)

    def push_fan_data(self, value):
        data = {
            "value" : value,
			"type" : "filter fan",
			"unit" : "",
			"time" : datetime.now()
        }

        self.fanCol.insert_one(data.copy())

        print("Filter fan: %s" % (data))
        data['time'] = str(data['time'])

        self.push_content(self._command_containers['FilterFan'], data)

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
        labels = []
        if sensor.startswith('Humi_in'):
            labels.append('humidity indoor')

            self.humiInCol = self.db[sensor]

        elif sensor.startswith('Humi_out'):
            labels.append('humidity outdoor')

            self.humiOutCol = self.db[sensor]
        
        elif sensor.startswith('Temp_in'):
            labels.append('temperature indoor')

            self.tempInCol = self.db[sensor]
        
        elif sensor.startswith('Temp_out'):
            labels.append('temperature outdoor')

            self.tempOutCol = self.db[sensor]

        elif sensor.startswith('PM2_5_in'):
            labels.append('PM2.5 indoor')

            self.pm25InCol = self.db[sensor]

        elif sensor.startswith('PM2_5_out'):
            labels.append('PM2.5 outdoor')

            self.pm25OutCol = self.db[sensor]

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
        if sensor.startswith('Humi_in'):
            data = {
                'value': value,
                'type': 'humidity indoor',
                'unit': 'percentage',
                'time': time
            }

            self.humiInCol.insert_one(data.copy())

        elif sensor.startswith('Humi_out'):
            data = {
                'value': value,
                'type': 'humidity outdoor',
                'unit': 'percentage',
                'time': time
            }

            self.humiOutCol.insert_one(data.copy())

        elif sensor.startswith('Temp_in'):
            data = {
                'value': value,
                'type': 'temperature indoor',
                'unit': 'degreeC',
                'time': time
            }

            self.tempInCol.insert_one(data.copy())

        elif sensor.startswith('Temp_out'):
            data = {
                'value': value,
                'type': 'temperature outdoor',
                'unit': 'degreeC',
                'time': time
            }

            self.tempOutCol.insert_one(data.copy())
            
        elif sensor.startswith('PM2_5_in'):
            data = {
                'value': value,
                'type': 'PM2.5 indoor',
                'unit': 'ug/m^3',
                'time': time
            }

            self.pm25InCol.insert_one(data.copy())

        elif sensor.startswith('PM2_5_out'):
            data = {
                'value': value,
                'type': 'PM2.5 outdoor',
                'unit': 'ug/m^3',
                'time': time
            }

            self.pm25OutCol.insert_one(data.copy())

        else:
            data = {
                'value': 0,
                'type': '',
                'unit': '',
                'time': time
            }

        # print the new data set
        print ("%s: %s" % (sensor, data))

        data['time'] = str(data['time'])

        # finally, push the data set to measurements_container of the sensor
        self.push_content(self._recognized_measurement_containers[sensor], data)

    def window_update(self):

        cursor_window = self.windowCol.find_one({}, sort=[('time', -1)])
        self.window_before = cursor_window["value"] if cursor_window != None else None

        if self.window_actuation != self.window_before:
            if cursor_window == None:
                print("\nWindow update: No data\n")
            else:
                id = cursor_window["_id"]
                type = cursor_window["type"]
                unit = cursor_window["unit"]
                time = cursor_window["time"]
                newID_window = ObjectId(generate())

                self.windowCol.delete_one({"_id": id})
                self.windowCol.insert_one({"_id": newID_window, "value": self.window_actuation, "type":type, "unit":unit, "time":time})

                cursor_window2 = self.windowCol.find_one({}, sort=[('time', -1)])

                print("\nWindow update: before: ", self.window_before, "after: ", cursor_window2["value"])
        else:
            print("\nWindow update: No state change in window actuation\n")


    def fan_update(self):

        cursor_fan = self.fanCol.find_one({}, sort=[('time', -1)])
        self.fan_before = cursor_fan["value"] if cursor_fan != None else None

        if self.fan_actuation != self.fan_before:
            if cursor_fan == None:
                print("\nFilter fan update: No data\n")
            else:
                id = cursor_fan["_id"]
                type = cursor_fan["type"]
                unit = cursor_fan["unit"]
                time = cursor_fan["time"]
                newID_fan = ObjectId(generate())

                self.fanCol.delete_one({"_id": id})
                self.fanCol.insert_one({"_id": newID_fan, "value": self.fan_actuation, "type":type, "unit":unit, "time":time})
                cursor_fan2 = self.fanCol.find_one({}, sort=[('time', -1)])

                print("\nFilter fan update: before: ", self.fan_before, "after: ", cursor_fan2["value"])
        else:
            print("\nFilter fan update: No state change in filterfan actuation\n")


if __name__ == "__main__":
    from openmtc_app.runner import AppRunner as Runner

    host = "http://localhost:8000#mn-cse-1"
    app = IPE(
        # SSL options
        name = 'HTTP_AQM',
        originator_pre='//openmtc.org/mn-cse-1',  # originator_pre, needs to match value in cert
        ca_certs='../../openmtc-gevent/certs/ca-chain.cert.pem',
        cert_file='certs/test-ipe.cert.pem',      # cert file, pre-shipped and should match name
        key_file='certs/test-ipe.key.pem'
    )
    Runner(app).run(host)
