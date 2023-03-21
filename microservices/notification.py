#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

from flask import Flask
from twilio.rest import Client
import json
import os
import requests

import amqp_setup

app = Flask(__name__)
app.config['TWILIO_ACCOUNT_SID'] = os.environ.get('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')
monitorBindingKey='*.notification' #e.g booking.notification; bidding.notification; listing.notification

sid = app.config['TWILIO_ACCOUNT_SID']
authToken = app.config['TWILIO_AUTH_TOKEN']
client = Client(sid, authToken)

def receiveNotification():
    amqp_setup.check_setup()
    
    queue_name = "Notification"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a notification by " + __file__)
    routing_key = method.routing_key
    processNotification(routing_key, body)
    print() # print a new line feed

#change to processNoti which calls the email api to send the noti
def processNotification(routing_key, body):
    print("in notification microservice")
    notification = json.loads(body)
    print(notification) 

    # Extract the "number" and "notification_info" keys from the notification object

    customer_id = notification["customer_id"]
    customer_URL = f"http://localhost:5000/customer/{customer_id}"
    response = requests.get(customer_URL)
    customer = response.json()
    name = customer['data']['name']
    number = customer['data']['phone']

    # Check the routing key to determine what type of notification to send
    if routing_key == "booking.notification":
        # Send a notification to the buyer that booking is confirmed
        message = client.messages.create(
            body=f"Dear {name}, your booking has been confirmed.",
            from_='+15077055450',
            to=f"+65{number}"
        )
        print(f"Sent booking notification to {number} via SMS")

    elif routing_key == "listing.notification":
        # Send a notification to the seller that the listing has been uploaded successfully
        message = client.messages.create(
            body=f"Dear {name}, your property has been listed.",
            from_='+15077055450',
            to=f"+65{number}"
        )
        print(f"Sent booking notification to {number} via SMS")

    else:
        # bidding.notification
        print("Sent bidding notification to highest bidder")

    return


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
