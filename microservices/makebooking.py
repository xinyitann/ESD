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

agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent/"
property_URL = environ.get('property_URL') or "http://localhost:5001/property/"
booking_URL = environ.get('booking_URL') or "http://localhost:5005/booking"


@app.route("/make_booking", methods=['POST'])
def make_booking():
    if request.is_json:
        try:
            data = request.get_json()
            result = processMakeBooking(data)
            if isinstance(result, str):
                return result
            return jsonify(result), result['code']
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "makebooking.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processMakeBooking(data):
    #invoke agent microservice
    get_agent_URL = agent_URL + "/" + str(data['agent_id'])
    agent_result = invoke_http(get_agent_URL, method='GET', json=data)
    if agent_result['code'] not in range(200,300):
        error_message = {
            "code": 400,
            "message": "Fail to add booking (agent microservice)"
        }
        print('\n\n-----Publishing the error message with routing_key=make_booking.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="make_booking.error",
                                            body=json.dumps(error_message),
                                            properties=pika.BasicProperties(delivery_mode=2))
        print("\nFail to add booking (agent microservice) published to the RabbitMQ Exchange.\n")

        return {
            "code": 400,
            "message": "Fail to add booking (agent microservice)"
        }

    print('agent result:', agent_result)
    
    #invoke property microservice
    get_property_URL = property_URL + "/" + str(data['property_id'])
    property_result = invoke_http(get_property_URL, method='GET', json=data)
    if property_result['code'] not in range(200,300):
        error_message = {
            "code": 400,
            "message": "Fail to add booking (property microservice)"
        }
        print('\n\n-----Publishing the error message with routing_key=make_booking.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="make_booking.error",
                                            body=json.dumps(error_message),
                                            properties=pika.BasicProperties(delivery_mode=2))
        print("\nFail to add booking (property microservice) published to the RabbitMQ Exchange.\n")

        return {
            "code": 400,
            "message": "Fail to add booking (property microservice)"
        }

    print('property result:', property_result)
    #invoke booking microservice
    booking_result = invoke_http(booking_URL, method='POST', json=data)
    if booking_result['code'] not in range(200,300):
        error_message = {
            "code": 400,
            "message": "Fail to add booking (booking microservice)"
        }
        print('\n\n-----Publishing the error message with routing_key=make_booking.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="make_booking.error",
                                            body=json.dumps(error_message),
                                            properties=pika.BasicProperties(delivery_mode=2))
        print("\nFail to add booking (booking microservice) published to the RabbitMQ Exchange.\n")

        return {
            "code": 400,
            "message": "Fail to add booking (booking microservice)"
        }
    
    combine = {}
    for item in agent_result['data']:
        if item not in combine:
            combine[item] = agent_result['data'][item]
    for item in property_result['data']:
        if item == 'name':
            combine['property_name'] = property_result['data'][item]
        if item not in combine:
            combine[item] = property_result['data'][item]
    combine['code'] = 200
    print(combine)
    return combine


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5800, debug=True)
