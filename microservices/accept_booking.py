from datetime import timedelta
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

booking_URL = environ.get('booking_URL') or "http://localhost:5005/booking"
customer_URL = environ.get('customer_URL') or "http://localhost:5700/customer"
property_URL = environ.get('property_URL') or "http://localhost:5001/property"
agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent"

def validate_booking_input(booking_details):
    # will have to get agent_id from agent profile somehow
    required_fields = ['agent_id', 'customer_id', 'booking_id', 'property_id', 'status']

    for field in required_fields:
        if field not in booking_details:
            return False
    return True

@app.route("/accept_booking", methods=['PUT'])
def accept_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_details = request.get_json()
            print("\nReceived a booking in JSON:", booking_details)

            # Validate accept booking input
            if not validate_booking_input(booking_details):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid accept booking input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (booking input error) message with routing_key=booking.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
                        body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2)) 
                print("\nInvalid booking input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid accept booking input: missing or invalid required fields."
                }), 400


            # accept a booking 
            booking_result = processAcceptBooking(booking_details)
            print("booking_result outside " , booking_result)
            print("customer_id ", booking_result["data"]['booking_result']["data"]["customer_id"])

            # get the customer id
            customer_id = booking_result["data"]['booking_result']["data"]["customer_id"]

            # get the agent id
            agent_id = booking_result["data"]['booking_result']["data"]["agent_id"]
            
            # check what is the status of the ticket
            status = booking_result["data"]['booking_result']["data"]["status"]

            # get the customer email and name 
            customer_info_result = get_customer_info(customer_id)
            print("customer_info_result ", customer_info_result)

            customer_email = customer_info_result["data"]['customer_result']["data"]["email"]
            customer_name =  customer_info_result["data"]['customer_result']["data"]["name"]

            # get the agent name 
            agent_info_result = get_agent_info(agent_id)
            print("agent_info_result ", agent_info_result)
            agent_name = agent_info_result["data"]['agent_result']["data"]["name"]
            print("agent_name ", agent_name)

            property_id = booking_details["property_id"]
            
            # get the name of the property
            property_info_result = get_property_info(property_id)
            print("property_info_result ", property_info_result)
            property_name = property_info_result["data"]["property_result"]["data"]["name"]

            start_time = booking_result["data"]['booking_result']["data"]["datetimestart"]
            start_time = datetime.datetime.strptime(start_time,'%a, %d %b %Y %H:%M:%S GMT')

            # if the status is accepted
            if booking_result['code'] == 201 and status == "accepted":
                
                # get the start and end data of the booking
                end_time = booking_result["data"]['booking_result']["data"]["datetimeend"]
                # end_time =start_time + timedelta(hours=1)
                end_time = datetime.datetime.strptime(end_time,'%a, %d %b %Y %H:%M:%S GMT')

                google_booking = {
                    "customer_id" : customer_id,
                    "start": start_time.strftime("%Y-%m-%dT%H:%M:%S"), 
                    "end": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "property_name": property_name, 
                    "customer_name": customer_name
                } 

                # add the booking into google calendar (with the customer and property name)
                print("google_booking ", google_booking)
                google_result = add_google_calendar(google_booking)
                print('\n------------------------')
                print('\ngoogle_result: ', google_result)
                
            
            # send the customer notification
            send_customer_notification(customer_name, customer_email, status, property_name, start_time.strftime("%Y-%m-%dT%H:%M:%S"), agent_name)
            print('\nbooking_result: ', booking_result) 
            return jsonify(booking_result), booking_result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "accept_booking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAcceptBooking(booking):
    print('\n-----Invoking booking microservice-----')
    update_booking_url = booking_URL + "/" + str(booking["booking_id"])
    # update the booking status to "accepted" or "rejected"
    booking_result = invoke_http(update_booking_url, method='PUT', json=booking)
    print('booking_result from booking microservice:', booking_result)

    code = booking_result["code"]
    message = json.dumps(booking_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=booking.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nbooking status ({:d}) published to the RabbitMQ Exchange:".format(
            code), booking_result)

        print("\nbooking published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"booking_result": booking_result},
            "message": "booking creation failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "booking_result": booking_result,
    }
}

def add_google_calendar(gooogle_booking):
    # Invoke the google calendar microservice in booking microservice
    print('\n-----Invoking google calendar microservice in booking-----')
    google_URL = booking_URL + "/create_event"
    # if the booking is accepted add the booking into the google calendar
    google_booking_result = invoke_http(google_URL, method='POST', json=gooogle_booking)
    print('google_booking_result:', google_booking_result)
    

    # Check the google booking result result; if a failure, send it to the error microservice.
    code = google_booking_result["code"]
    message = json.dumps(google_booking_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=property.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("booking status ({:d}) published to the RabbitMQ Exchange:".format(
            code), google_booking_result)

        print("booking published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"google_booking_result": google_booking_result},
            "message": "booking creation failure sent for error handling."
        }

    # if reached here, no error & booking in google calendar is successfully created
    return {
        "code": 201,
        "data": {
            "google_booking_result": google_booking_result,
        }
    }

# get the customer info
def get_customer_info(customer_id):
    print('\n-----Invoking customer microservice -----')
    customer_id = str(customer_id)
    get_customer_URL = customer_URL + "/" + customer_id
    customer_result = invoke_http(get_customer_URL, method='GET', json=None)

    code = customer_result["code"]
    message = json.dumps(customer_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=property.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("booking status ({:d}) published to the RabbitMQ Exchange:".format(
            code), customer_result)

        print("booking published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"customer_result": customer_result},
            "message": "unable to find customer."
        }

    # if reached here, no error & booking in google calendar is successfully created
    return {
        "code": 201,
        "data": {
            "customer_result": customer_result,
        }
    }


# get the agent info
def get_agent_info(agent_id):
    print('\n-----Invoking agent microservice -----')
    agent_id = str(agent_id)
    get_agent_URL = agent_URL + "/" + agent_id
    agent_result = invoke_http(get_agent_URL, method='GET', json=None)

    code = agent_result["code"]
    message = json.dumps(agent_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=property.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("booking status ({:d}) published to the RabbitMQ Exchange:".format(
            code), agent_result)

        print("booking published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"agent_result": agent_result},
            "message": "unable to find agent."
        }

    # if reached here, no error & booking in google calendar is successfully created
    return {
        "code": 201,
        "data": {
            "agent_result": agent_result,
        }
    }

# get the property info using property_id
def get_property_info(property_id):
    print('\n-----Invoking property microservice -----')
    property_id = str(property_id)
    get_property_URL = property_URL + "/details/" + property_id
    property_result = invoke_http(get_property_URL, method='GET', json=None)

    code = property_result["code"]
    message = json.dumps(property_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=property.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("booking status ({:d}) published to the RabbitMQ Exchange:".format(
            code), property_result)

        print("booking published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"property_result": property_result},
            "message": "unable to find customer."
        }

    # if reached here, no error & booking in google calendar is successfully created
    return {
        "code": 201,
        "data": {
            "property_result": property_result,
        }
    }

def send_customer_notification(name, email, status, property_name, start_time, agent_name):
        # customer_id = str(customer_id)
        # get_customer_URL = customer_URL + "/" + customer_id
        # # get the customer email
        # customer_result = invoke_http(get_customer_URL, method='GET', json=None)

        name_email = {
            'name' : name,
            'email' : email,
            'property_name': property_name, 
            'start_time': start_time,
            "agent_name": agent_name
        }

        # if the status is accepted send the customer the accepted notification
        if status == "accepted":
            print('\n\n-----Calling Notification with routing_key=booking_accepted.notification-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking_accepted.notification", 
            body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 
        
        # if the status is rejected send the customer the rejected notification
        elif status == "rejected":
            print('\n\n-----Calling Notification with routing_key=booking_rejected.notification-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking_rejected.notification", 
            body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting booking...")
    app.run(host="0.0.0.0", port=5101, debug=True)
