import paho.mqtt.client as mqtt
import json

class Company:
    def __init__(self, name, pizza_list):
        self.name = name
        self.pizza_list = pizza_list

companies = []

def on_connect(client, userdata, flags, rc):
    client.subscribe([                    
                    ("hshl/company/company3", 2),
                    ])

def on_message(client, userdata, msg):
    print(str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)


data = {
    "name": "Pizza Company 3", 
    "pizza_list" :["Greek Pizza"], 
    "topic": "hshl/company/company3"
    }
client.publish("hshl/server/company", json.dumps(data))

client.loop_forever()