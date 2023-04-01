from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

property_URL = environ.get('property_URL') or "http://localhost:5001/property"
bid_URL = environ.get('bid_URL') or "http://localhost:5500/bids"


@app.route("/getbids/<string:customer_id>", methods=['GET'])
def get_bids(customer_id):    
    
    # if request.is_json:
        try:
            print("\nReceived a customer ID in JSON:", customer_id)

            # do the actual work
            result = process_get_bids(customer_id)
            return jsonify(result), result["code"]

            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "get_bids.py internal error: " + ex_str
            }), 500

    # # if reached here, not a JSON request.
    # return jsonify({
    #     "code": 400,
    #     "message": "Invalid JSON input: " + str(request.get_data())
    # }), 400

def process_get_bids(customer_id):

    # call bids microservice to get the bids details for specific customer_id
    print('\n-----Invoking bids microservice-----')
    get_bids_url = bid_URL + "/customer_bids/" + str(customer_id)
    bids_result = invoke_http(get_bids_url, method='GET', json=None)
    print('bids_result:', bids_result)

    # get a list of auction_ids from the bids_result
    auction_id_list = []
    for bid in bids_result["data"]:
        auction_id_list.append(bid['auction_id'])
    
    # call property microservice to get all properties that are in list of auction_ids
    print('\n-----Invoking property microservice-----')
    property_result = []

    for auction_id in auction_id_list:
        get_property_url = property_URL + "/details/auction/" + str(auction_id)
        property_result.append(invoke_http(get_property_url, method='GET', json=None)["data"]["property"])

    print('property_result:', property_result)


    # return the property details and agent details and if user have bid
    return {
        "code": 201,
        "data": {
        "bids_result": bids_result["data"],
        "property_result": property_result
        }
    }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for searching...")
    app.run(host="0.0.0.0", port=5029, debug=True)