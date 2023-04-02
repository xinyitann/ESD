#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

from flask import Flask
from email.message import EmailMessage
import ssl
import smtplib
import json
import os
import requests

import amqp_setup

app = Flask(__name__)
email_sender = 'havenis213@gmail.com'
email_password = os.environ.get('EMAIL_PASSWORD') 
monitorBindingKey='*.notification' #e.g booking.notification; bidding.notification; listing.notification


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
    em = EmailMessage()
    em['From'] = email_sender
    print("in notification microservice")
    notification = json.loads(body)
    print(notification) 

    name = notification['name']
    email_receiver = notification['email']

    # Check the routing key to determine what type of notification to send
    if routing_key == "booking_accepted.notification":
        # Send a notification to the buyer that schedule is confirmed successfully
        booking_date = notification["start_time"]
        property_name = notification["property_name"]
        agent_name = notification["agent_name"]

        content = f"""
        Hey {name}, \n
        I am writing to inform you that your schedule on {booking_date} regarding the property {property_name} with our agent {agent_name} has been confirmed. Your agent will be contacting you shortly. \n
        If you have any questions or concerns, please do not hesitate to contact us at havenis213@gmail.com. \n
        Thank you for choosing Haven! \n

        Best regards, \n
        G2T4 Haven Team
        """
        em['To'] = email_receiver
        em['Subject'] = "Booking Confirmation"
        em.set_content(content)

    elif routing_key == "booking_rejected.notification":
        # Send a notification to the buyer that schedule needs to be rebooked because agent rejected
        booking_date = notification["start_time"]
        property_name = notification["property_name"]
        agent_name = notification["agent_name"]
        
        content = f"""
        Hey {name}, \n
        I am writing to inform you that your schedule on {booking_date} regarding the property {property_name} with our agent {agent_name} has been rejected. Please rebook your appointment with our agent. \n
        If you have any questions or concerns, please do not hesitate to contact us at havenis213@gmail.com. \n
        Thank you for choosing Haven! \n

        Best regards, \n
        G2T4 Haven Team
        """

        em['To'] = email_receiver
        em['Subject'] = "Booking Rejected"
        em.set_content(content)

    elif routing_key == "listing.notification":
        # Send a notification to the seller that the listing has been uploaded successfully
        agent_name = notification["agent_name"]
        content = f"""
        Hey {name}, \n
        I am writing to inform you that your listing has been successfully uploaded to our platform by agent {agent_name}. Your listing is now visible to our users and you can expect to receive inquiries and offers shortly. \n
        If you have any questions or concerns, please do not hesitate to contact us at havenis213@gmail.com. \n
        Thank you for choosing Haven! \n

        Best regards, \n
        G2T4 Haven Team
        """
        em['To'] = email_receiver
        em['Subject'] = "Property Listed"
        em.set_content(content)

    else:
        # bidding.notification
        property_name= notification['property_name']
        option_fee = notification['option_fee']
        payment_URL = f"http://localhost:8080/optionfee={option_fee}"
        print(option_fee)
        content = f"""
        Hey {name}, \n
        I am writing to inform you that you are the highest bidder for the property. Congratulations on winning the bid! \n

        Here are the details of your bid: \n

        Property Title: {property_name}  \n
        Option Fee: {option_fee} \n

        As the highest bidder, you are now required to proceed with the payment for the property within the next [insert payment duration here] days. You can make the payment by {payment_URL}. \n

        Please note that if you fail to make the payment within the specified time, we reserve the right to offer the property to the next highest bidder or relist it for auction. \n

        If you have any questions or concerns, please do not hesitate to contact us at havenis213@gmail.com. \n
        Thank you for choosing Haven! \n

        Best regards, \n
        G2T4 Haven Team
        """
        em['To'] = email_receiver
        em['Subject'] = "Congratulations! You are the highest bidder for the property"
        em.set_content(content)

    message_string = em.as_string()
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, message_string)
    print(f"Sent bidding results to {email_receiver} via email")

    return


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
