import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime

# Create an "on_message" callback function (event handler) for the "on_message" event
def on_message(client, userdata, message):
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")


print("creating new instance")
client2 = mqtt.Client("P2")     # create new instance (the ID, in this case "P1", must be unique)

#broker_address = "localhost" # Use your own MQTT Server IP Adress (or domain name) here, or ...
broker_address = "test.mosquitto.org" # ... use the Mosquitto test server during development

# Use exception handling (try...except in Python)
try:
    print("connecting to broker")
    client2.connect(broker_address) # connect to broker
    

    print("Subscribing to topic: teds22/group06/pressure")
    client2.subscribe("teds22/group06/pressure",qos=2) # subscribe

    client2.on_message = on_message 
    
    client2.loop_forever()

    #print("Unsubscribing from topic: teds22/group06/pressure")
    #client2.unsubscribe("teds22/group06/pressure") # unsubscribe

    #time.sleep(4)       # wait 4 seconds before stopping the event processing loop (so all pending events are processed)
    #client2.loop_stop()  # stop the event processing loop

    #print("\ndisconnecting from broker")
    #client2.disconnect() # disconnect from broker
except Exception as e:
    # if we receive an exception (error) in the "try" block,
    # handle it here, by printing out the error message
    print(f"connection error: {e}")