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

def validate_property_input(property):
    required_fields = ['agent_id', 'customer_id', 'name', 'address', 'postalcode', 'property_type', 'square_feet', 'room', 'facing', 'build_year', 'estimated_cost', 'image']

    for field in required_fields:
        if field not in property:
            return False
    return True

@app.route("/add_listing", methods=['POST'])
def add_listing():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            property = request.get_json()
            print("\nReceived a property listing in JSON:", property)

            # Validate property input
            if not validate_property_input(property):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid property input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (property input error) message with routing_key=property.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="property.error",
                                                 body=json.dumps(error_message),
                                                 properties=pika.BasicProperties(delivery_mode=2))
                print("\nInvalid property input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid property input: missing or invalid required fields."
                }), 400


            # 1. Send property info {`agent_id`,`customer_id`, `name`, `address`, `postalcode`,`property_type`, `square_feet`, `room`, `facing`,`build_year`, `estimated_cost`,`image`}
            result = processAddListing(property)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

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

        # 7. Return error
        return {
            "code": 500,
            "data": {"property_result": property_result},
            "message": "property creation failure sent for error handling."
        }
   
    print("\nproperty published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

    # 7. Return created property
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
