import paho.mqtt.client as mqtt
import json

class Company:
    def __init__(self, name, pizza_list):
        self.name = name
        self.pizza_list = pizza_list

companies = []

def on_connect(client, userdata, flags, rc):
    client.subscribe([                    
                    ("hshl/company/company1", 2),
                    ])

def on_message(client, userdata, msg):
    print(str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("FlespiToken HrgInVHyjGwFVFt4ykQuQKlLY4uc5oBCDHaRqGdxcx2W2lQovuJa2ULRM5RGhi8L")
client.connect("mqtt.flespi.io", 1883, 60)


data = {
    "name": "Pizza Company 1", 
    "pizza_list" :["Vegetarian", "Salami"], 
    "topic": "hshl/company/company1"
    }
client.publish("hshl/server/company", json.dumps(data))

client.loop_forever()