# left to do the rejected part 
# link to the js file instead of the py one

from datetime import timedelta
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

booking_URL = "http://127.0.0.1:5005/booking"
customer_URL = "http://localhost:5700/customer"

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


            booking_result = processAcceptBooking(booking_details)
            print("booking_result outside " , booking_result)
            print("customer_id ", booking_result["data"]['booking_result']["data"]["customer_id"])
            customer_id = booking_result["data"]['booking_result']["data"]["customer_id"]
            
            status = booking_result["data"]['booking_result']["data"]["status"]

            if booking_result['code'] == 201 and status == "accepted":
                

                start_time = booking_result["data"]['booking_result']["data"]["datetime"]
                start_time = datetime.datetime.strptime(start_time,'%a, %d %b %Y %H:%M:%S GMT')
                end_time =start_time + timedelta(hours=1)

                google_booking = {
                    "customer_id" : customer_id,
                    "start": start_time.strftime("%Y-%m-%dT%H:%M:%S"), 
                    "end": end_time.strftime("%Y-%m-%dT%H:%M:%S")
                } 

                google_result = add_google_calendar(google_booking)
                print('\n------------------------')
                print('\ngoogle_result: ', google_result)
                
            
            send_customer_notification(customer_id, status)
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
    else: 
        # print('\n\n-----Calling Notification with routing_key=listing.notification-----')

        # customer_id = str(gooogle_booking["customer_id"])
        # get_customer_URL = customer_URL + "/" + customer_id
        # customer_result = invoke_http(get_customer_URL, method='GET', json=None)

        # name_email = {
        #     'name' : customer_result['data']['name'],
        #     'email' : customer_result['data']['email']
        # }

        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="listing.notification", 
        # body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "data": {
                "google_booking_result": google_booking_result,
            }
        }


def send_customer_notification(customer_id, status):
        customer_id = str(customer_id)
        get_customer_URL = customer_URL + "/" + customer_id
        customer_result = invoke_http(get_customer_URL, method='GET', json=None)

        name_email = {
            'name' : customer_result['data']['name'],
            'email' : customer_result['data']['email']
        }

        if status == "accepted":
            print('\n\n-----Calling Notification with routing_key=booking_accepted.notification-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking_accepted.notification", 
            body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 
        
        elif status == "rejected":
            print('\n\n-----Calling Notification with routing_key=booking_rejected.notification-----')
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking_rejected.notification", 
            body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting booking...")
    app.run(host="0.0.0.0", port=5101, debug=True)