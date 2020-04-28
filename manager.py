import paho.mqtt.client as mqtt
import json

class Company:
    def __init__(self, name, pizza_list, topic):
        self.name = name
        self.pizza_list = pizza_list
        self.topic = topic

companies = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([
                    ("hshl/server/order", 2), 
                    ("hshl/server/company", 2),
                    ])

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic.endswith('company')):
        register_company(msg.payload)
    if(msg.topic.endswith('order')):
        process_order(msg.payload)

def process_order(data):
    js = json.loads(data)
    name = js['name']
    pizza = js['pizza']
    quantity = js['quantity']
    topic = js['topic']

    selected_company = None

    for company in companies:
        if pizza in company.pizza_list:
            selected_company = company

    response = ''
    if selected_company != None:
        response = 'The company '+selected_company.name+ ' will deliver your pizza'
        client.publish(selected_company.topic, name+ ' wants '+quantity+ ' pizzas '+pizza)
    else:
        response = 'Sorry, nobody has this kind of pizza'
    
    client.publish(topic, response)
 

def register_company(data):
    js = json.loads(data)
    company = Company(js['name'], js['pizza_list'], js['topic'])
    companies.append(company)
    print('#####################')
    for c in companies:
        print(c.name)
        print(c.pizza_list)
        print('--------------')
    print('#####################')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()