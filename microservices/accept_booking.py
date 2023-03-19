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

@app.route("/add_booking", methods=['POST'])
def add_booking():
    booking = request.get_json()
    print("\nReceived a booking request in JSON:", booking)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.notification", 
        body=json.dumps(booking), properties=pika.BasicProperties(delivery_mode = 2)) 

    return {
        "code": 201,
        "data": {
            "notification sent": 'yes',
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting booking...")
    app.run(host="0.0.0.0", port=5101, debug=True)