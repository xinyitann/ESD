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

property_URL = "http://localhost:5001/property"
auction_URL = "http://localhost:5002/auctions"

def validate_property_input(listing_details):
    # will have to get agent_id from agent profile somehow
    required_fields = ['agent_id', 'customer_id', 'name', 'address', 'postalcode', 'property_type', 'square_feet', 'room', 'facing', 'build_year', 'estimated_cost', 'image', 'start_time', 'end_time', 'starting_price', 'option_fee']

    for field in required_fields:
        if field not in listing_details:
            return False
    return True

@app.route("/add_listing", methods=['POST'])
def add_listing():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing_details = request.get_json()
            print("\nReceived a property listing in JSON:", listing_details)

            # Validate property input
            if not validate_property_input(listing_details):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid listing input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (listing input error) message with routing_key=property.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="property.error",
                                                 body=json.dumps(error_message),
                                                 properties=pika.BasicProperties(delivery_mode=2))
                print("\nInvalid listing input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid listing input: missing or invalid required fields."
                }), 400

            auction_data = {
                'start_time': listing_details['start_time'],
                'end_time': listing_details['end_time'],
                'starting_price': listing_details['starting_price'],
                'option_fee': listing_details['option_fee'],
                'auction_id': None
            }

            auction_result = processAddAuction(auction_data)
            print("before gg into ")
            if auction_result['code'] == 201:
                print("inside")
                print(auction_result['data']['auction_result']['data']['auction_id'])
                property_data = {
                    'auction_id': auction_result['data']['auction_result']['data']['auction_id'],
                    'agent_id': listing_details['agent_id'],
                    'customer_id': listing_details['customer_id'],
                    'name': listing_details['name'],
                    'address': listing_details['address'],
                    'postalcode': listing_details['postalcode'],
                    'property_type': listing_details['property_type'],
                    'square_feet': listing_details['square_feet'],
                    'room': listing_details['room'],
                    'facing': listing_details['facing'],
                    'build_year': listing_details['build_year'],
                    'estimated_cost': listing_details['estimated_cost'],
                    'image': listing_details['image']
                }

                property_result = processAddListing(property_data)
                print('\n------------------------')
                print('\nproperty_result: ', property_result)
                print('\nauction_result: ', auction_result)
                return jsonify(property_result), property_result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_property.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAddAuction(auction_data):
    print('\n-----Invoking auction microservice-----')
    auction_result = invoke_http(auction_URL, method='POST', json=auction_data)
    print('auction_result from auction microservice:', auction_result)

    code = auction_result["code"]
    message = json.dumps(auction_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (property error) message with routing_key=property.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="auction.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
            code), auction_result)

        print("\nauction published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"auction_result": auction_result},
            "message": "auction creation failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "auction_result": auction_result,
    }
}

def processAddListing(property):
    # Invoke the property microservice
    print('\n-----Invoking property microservice-----')
    property_result = invoke_http(property_URL, method='POST', json=property)
    print('property_result:', property_result)
    

    # Check the property result; if a failure, send it to the error microservice.
    code = property_result["code"]
    message = json.dumps(property_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (property error) message with routing_key=property.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="property.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nproperty status ({:d}) published to the RabbitMQ Exchange:".format(
            code), property_result)

        print("\nproperty published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"property_result": property_result},
            "message": "property creation failure sent for error handling."
        }

    # if reached here, no error & property is successfully created
    else: 
        print('\n\n-----Calling Notification with routing_key=listing.notification-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="listing.notification", 
        body=json.dumps(property), properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "data": {
                "property_result": property_result,
            }
        }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for adding a property...")
    app.run(host="0.0.0.0", port=5100, debug=True)
