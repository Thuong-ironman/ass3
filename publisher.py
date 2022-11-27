import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime

# Create an "on_message" callback function (event handler) for the "on_message" event
def on_message(client, userdata, message):
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")
    print(f"message topic: {message.topic}")
    print(f"message qos: {message.qos}")
    print(f"message retain flag: {message.retain}")

print("creating new instance")
client = mqtt.Client("P1")     # create new instance (the ID, in this case "P1", must be unique)
client.on_message = on_message # attach "on_message" callback function (event handler) to "on_message" event

def simulated_pressure(mu, sigma):
    mu = 1200.00
    sigma = 1.0
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'
    return message 

#broker_address = "localhost" # Use your own MQTT Server IP Adress (or domain name) here, or ...
broker_address = "test.mosquitto.org" # ... use the Mosquitto test server during development

# Use exception handling (try...except in Python)
try:
    print("connecting to broker")
    client.connect(broker_address) # connect to broker
    client.loop_start()            # start the event processing loop

    print("Subscribing to topic: teds22/group06/pressure")
    client.subscribe("teds22/group06/pressure") # subscribe
    
    i = 0
    for i in range(10):
        print("Publishing message {} to topic: teds22/group06/pressure".format(simulated_pressure(10, 1)))
        client.publish("teds22/group06/pressure", simulated_pressure(10,1), qos=2) # publish
        time.sleep(1)
        i += i


    print("Unsubscribing from topic: teds22/group06/pressure")
    client.unsubscribe("teds22/group06/pressure") # unsubscribe

    time.sleep(4)       # wait 4 seconds before stopping the event processing loop (so all pending events are processed)
    client.loop_stop()  # stop the event processing loop

    print("\ndisconnecting from broker")
    client.disconnect() # disconnect from broker
except Exception as e:
    # if we receive an exception (error) in the "try" block,
    # handle it here, by printing out the error message
    print(f"connection error: {e}")