from datetime import timedelta
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/property_management')
auction_URL = "http://localhost:5002/auctions"
customer_URL = "http://localhost:5700/customer"

def validate_close_bid_input(closing_details):
    required_fields = ['auction_id', 'status']

    for field in required_fields:
        if field not in closing_details:
            return False
    return True

@app.route("/close_bid", methods=['PUT'])
def close_bid():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            close_bid_details = request.get_json()
            print("\nReceived a close bid request in JSON:", close_bid_details)

            # Validate accept booking input
            if not validate_close_bid_input(close_bid_details):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid close bid input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (bidding input error) message with routing_key=bidding.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
                        body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2)) 
                print("\nInvalid closing input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid closing input: missing or invalid required fields."
                }), 400

            # will close the bidding
            close_bid_result = processCloseBid(close_bid_details)
            
            print("close_bid_result outside " , close_bid_result)
            
            if close_bid_result['code'] == 201:
                # get highest bidder customer id and send them a notification
                highest_bid_result = get_highest_bid(close_bid_details)

                print('\n------------------------')
                print('\nhighest_bid_result: ', highest_bid_result)
                return jsonify(highest_bid_result), highest_bid_result["code"]
                            

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "close_bid.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def get_highest_bid(close_bid):
    print('\n-----Invoking auction microservice-----')
    highest_URL = auction_URL + "/" + str(close_bid["auction_id"])
    # get the customer id of the highest bidder
    higest_bid_result = invoke_http(highest_URL, method='GET', json=None)
    print('higest_bid_result from auction microservice:', higest_bid_result)

    code = higest_bid_result["code"]
    message = json.dumps(higest_bid_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (get highest bidder error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nfailed highest bidder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), higest_bid_result)

        print("\nget highest bid published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"higest_bid_result": higest_bid_result},
            "message": "getting highest bidder failure sent for error handling."
        }
    else:
        print('\n\n-----Calling Notification with routing_key=bidding.notification-----')

        # Retrieve the property name associated with the auction ID
        auction_id = close_bid["auction_id"]
        query = f"SELECT name FROM property WHERE auction_id={auction_id}"
        with engine.connect() as conn:
            result = conn.execute(query)
            property_name = result.fetchone()[0]

        # Retrieve the customer details associated with the highest bid
        customer_id = higest_bid_result["data"]
        get_customer_URL = customer_URL + "/" + str(customer_id)
        customer_result = invoke_http(get_customer_URL, method='GET', json=None)

        #Create the name_email dictionary with the customer name, email, and property name
        name_email_property = {
            'name' : customer_result['data']['name'],
            'email' : customer_result['data']['email'],
            'property_name' : property_name
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.notification", 
        body=json.dumps(name_email_property), properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "data": {
                "higest_bid_result": higest_bid_result,
            }
        }

    

def processCloseBid(close_bid_details):
    # Invoke the auction microservice
    print('\n-----Invoking auction microservice-----')
    close_URL = auction_URL +  "/" + str(close_bid_details["auction_id"]) + "/close"
    # change the status of the auction to close
    close_auction_result = invoke_http(close_URL, method='PUT', json=close_bid_details)
    print('close_auction_result:', close_auction_result)
    

    # Check the close auction result; if a failure, send it to the error microservice.
    code = close_auction_result["code"]
    message = json.dumps(close_auction_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (closing auction error) message with routing_key=bidding.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("closing status ({:d}) published to the RabbitMQ Exchange:".format(
            code), close_auction_result)

        print("closing auction published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"close_auction_result": close_auction_result},
            "message": "booking creation failure sent for error handling."
        }

    # else return the close auction details
    return {
        "code": 201,
        "data": {
            "close_auction_result": close_auction_result,
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting booking...")
    app.run(host="0.0.0.0", port=5801, debug=True)