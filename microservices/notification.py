#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

from twilio.rest import Client
import json
import os

import amqp_setup

monitorBindingKey='*.notification' #e.g booking.notification; bidding.notification

sid =''
authToken = ''
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
    processNotification(body)
    print() # print a new line feed

#change to processNoti which calls the email api to send the noti
def processNotification(body):
    print("in notification microservice")
    # Parse the JSON message body
    booking = json.loads(body)

    # Extract the "number" and "booking_info" keys from the booking object
    number = booking["number"]
    booking_info = booking["booking_info"]

    # Send the notification to the specified number using Twilio API
    client = Client(sid, authToken)
    message = client.messages.create(
        body=booking_info,
        from_='whatsapp:+14155238886',
        to=f"whatsapp:+65{number}"
    )

    print(f"Sent notification to {number} via WhatsApp")
    return


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
