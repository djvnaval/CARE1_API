# virtually the actuator that adhere to oneM2M standard
# Smart Farm Solenoid Valve actuator

from random import random
from datetime import datetime

from openmtc_app.onem2m import XAE
from openmtc_onem2m.model import Container
import pymongo

MONGO_URI = 'mongodb+srv://onem2mCARE1:onem2mCARE1diliman@onem2m.up2wghs.mongodb.net/?retryWrites=true&w=majority'


class SPICEActuator(XAE):
    remove_registration = True
    remote_cse = '/mn-cse-1/onem2m'

    def _on_register(self):
        self.actuators = ['SolenoidValve']
        
        self._command_containers = {}
        #self_actuators = []
        '''
        self.periodic_discover(
            self.remote_cse,                # start directory inside cse for discovery
            {'labels': ['commands']},       # filter criteria (what to discover)
            1,                              # frequency of repeated discovery (in Hz)
            self.handle_discovery_commands  # callback function to return the result of the discovery to)
        )
        '''

        label = 'devices_mqtt'
        container = Container(resourceName=label)
        self._devices_container = self.create_container(None,
                                                        container,
                                                        labels=[label],
                                                        max_nr_of_instances=0)
        
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
                labels=['commands-measurement']
            )
            # add commands_container of current actuator to self._command_containers
            self._command_containers[actuator] = commands_container
            self.add_container_subscription(
                commands_container.path,    # the Container or it's path to be subscribed
                self.handle_command         # reference of the notification handling function
            )
        

        self.run_forever(5, self.push_actuation_data)

        # log message
        self.logger.debug('registered')
        

    def handle_discovery_commands(self, discovery):
        for uri in discovery:
            print("discovered command container: %s" % uri)
            self.add_container_subscription(uri, self.handle_command)

    def get_actuation_data(self):
        
        cursor = col_actuation.find_one({}, sort=[('time', -1)])

        if cursor == None:
            actuation = 0
        else:
            actuation = cursor["value"]

        return actuation
    
    def handle_command(self):

        data = {
            "value" : self.get_actuation_data,
			"type" : "solenoid valve",
			"unit" : "none",
			"time" : str(datetime.datetime.now())
        }
        print("Solenoid valve command: %s" % (data))
        for actuator in self.actuators:
            if 'SolenoidValve' in actuator:
                self.push_content(actuator, data)

    def push_actuation_data(self):
        value = self.get_actuation_data()

        data = {
            "value" : self.get_actuation_data(),
			"type" : "solenoid valve",
			"unit" : "none",
			"time" : str(datetime.now())
        }
        print("Solenoid valve command: %s" % (data))
        
        self.push_content(self._command_containers['SolenoidValve'], data)



if __name__ == "__main__":

    from openmtc_app.runner import AppRunner as Runner

    # Setup MongoDB connection
    mongo_client = pymongo.MongoClient(MONGO_URI)

    db = mongo_client.oneM2M_MQTT_SmartFarm
    col_actuation = db.solenoidValve

    host = "mqtts://spiceActuator:spiceAct1@29c49bdf585f4e6d8e93e1522dc5e23f.s1.eu.hivemq.cloud:8883#mn-cse-1"
    app = SPICEActuator(
        # SSL options
        name = 'MQTT_SmartFarm_actuate',
        originator_pre='//openmtc.org/mn-cse-1',  # originator_pre, needs to match value in cert
        ca_certs='../../openmtc-gevent/certs/ca-chain.cert.pem',
        cert_file='certs/test-ipe.cert.pem',      # cert file, pre-shipped and should match name
        key_file='certs/test-ipe.key.pem'
    )
    Runner(app).run(host)