from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent"
property_URL = environ.get('property_URL') or "http://localhost:5001/property"
bid_URL = environ.get('bid_URL') or "http://localhost:5500/bids"

@app.route("/get_property_details/<string:property_id>/<string:customer_id>", methods=['GET'])
def get_property_details(property_id,customer_id):    
    
    # if request.is_json:
        try:
            # property_id = request.get_json()
            print("\nReceived a property ID in JSON:", property_id)

            # do the actual work
            result = process_get_property_details(property_id,customer_id)
            return jsonify(result), result["code"]

            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "get_property_details.py internal error: " + ex_str
            }), 500

    # # if reached here, not a JSON request.
    # return jsonify({
    #     "code": 400,
    #     "message": "Invalid JSON input: " + str(request.get_data())
    # }), 400

def process_get_property_details(property_id,customer_id):

    # property_id = json_str["property_id"]
    # customer_id = json_str["customer_id"]

    # call property microservice to get the property details
    print('\n-----Invoking property microservice-----')
    get_property_url = property_URL + "/details/" + str(property_id)
    property_result = invoke_http(get_property_url, method='GET', json=None)
    print('property_result:', property_result)

    # call agent microservice to get agent information
    agent_id = property_result["data"]["agent_id"] 

    print('\n-----Invoking agent microservice-----')
    get_agent_url = agent_URL + "/" + str(agent_id)
    agent_result = invoke_http(get_agent_url, method='GET', json=None)
    print('agent_result:', agent_result)

    # call auction microservice to check if user bid for this property or not (will return true or false)
    auction_id = property_result["data"]["auction_id"]

    print('\n-----Invoking auction microservice-----')
    get_bid_url = bid_URL + "/" + str(auction_id) + "/" + str(customer_id)
    bid_result = invoke_http(get_bid_url, method='GET', json=None)
    print('bid_result:', bid_result)

    # return the property details and agent details and if user have bid
    return {
        "code": 201,
        "data": {
        "property_result": property_result,
        "agent_result": agent_result,
        "bid_result": bid_result
        }
    }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for searching...")
    app.run(host="0.0.0.0", port=5009, debug=True)