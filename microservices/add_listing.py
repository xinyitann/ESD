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

property_URL = environ.get('property_URL') or "http://localhost:5001/property"
auction_URL = environ.get('auction_URL') or "http://localhost:5002/auctions"
customer_URL = environ.get('customer_URL') or "http://localhost:5700/customer"
agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent"

def validate_property_input(listing_details):
    # will have to get agent_id from agent profile somehow
    required_fields = ['agent_id', 'customer_id', 'name', 'address', 'postalcode', 'property_type', 'neighbourhood', 'square_feet', 'room', 'facing', 'build_year', 'estimated_cost', 'image', 'status', 'starting_price', 'option_fee']

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
                'status': listing_details['status'],
                'starting_price': listing_details['starting_price'],
                'option_fee': listing_details['option_fee'],
                'auction_id': None,
                'customer_id': listing_details['customer_id'],
            }

            # add auction 
            auction_result = processAddAuction(auction_data)
            
            if auction_result['code'] == 201:
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
                    'image': listing_details['image'],
                    'neighbourhood': listing_details['neighbourhood']
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
        print('\n\n-----Publishing the (auction error) message with routing_key=auction.error-----')

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

    # if reach here, means auction is successfully added
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
        # get customer name and email from customer microservice
        customer_id = property["customer_id"]
        customer_result = get_customer_info(customer_id)

        # get agent name from agent microservice
        agent_id = property["agent_id"]
        agent_info_result = get_agent_info(agent_id)

        name_email = {
            'name' : customer_result["data"]["customer_result"]["data"]["name"],
            'email' : customer_result["data"]["customer_result"]["data"]["email"],
            'agent_name' : agent_info_result["data"]['agent_result']["data"]["name"]
        }
        print('\n\n-----Calling Notification with routing_key=listing.notification-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="listing.notification", 
        body=json.dumps(name_email), properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "data": {
                "property_result": property_result,
            }
        }

def get_customer_info(customer_id):
    print('\n-----Invoking customer microservice -----')
    customer_id = str(customer_id)
    get_customer_URL = customer_URL + "/" + customer_id
    customer_result = invoke_http(get_customer_URL, method='GET', json=None)

    code = customer_result["code"]
    message = json.dumps(customer_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (add_listing error) message due to failure to get customer info with routing_key=add_listing.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="add_listing.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("add_listing status ({:d}) published to the RabbitMQ Exchange:".format(
            code), customer_result)

        print("add_listing published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"customer_result": customer_result},
            "message": "unable to find customer."
        }

    # if reached here, no error & customer details can be retrieved
    return {
        "code": 201,
        "data": {
            "customer_result": customer_result,
        }
    }

def get_agent_info(agent_id):
    print('\n-----Invoking agent microservice -----')
    agent_id = str(agent_id)
    get_agent_URL = agent_URL + "/" + agent_id
    agent_result = invoke_http(get_agent_URL, method='GET', json=None)

    code = agent_result["code"]
    message = json.dumps(agent_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (add_listing error) message due to failure to get agent info with routing_key=add_listing.error-----')


        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="add_listing.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("add_listing status ({:d}) published to the RabbitMQ Exchange:".format(
            code), agent_result)

        print("add_listing published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"agent_result": agent_result},
            "message": "unable to find agent."
        }

    # if reached here, means no error & agent details can be retrieved
    return {
        "code": 201,
        "data": {
            "agent_result": agent_result,
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for adding a property listing...")
    app.run(host="0.0.0.0", port=5200, debug=True)
