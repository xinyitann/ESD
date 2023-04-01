from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent"
customer_URL = environ.get('customer_URL') or "http://localhost:5700/customer"

@app.route("/profile_page/<id>/<type>", methods=['GET'])
def get_profile(id,type):
    if True:
        try:
            result = processMakeBookingg(id,type)
            print(result)
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

def processMakeBookingg(id,type):
    get_agent_URL = agent_URL + str(id)
    get_customer_URL = customer_URL + str(id)
    #invoke agent microservice
    if type == 'agent':
        agent_result = invoke_http(get_agent_URL, method='GET')
        if agent_result['code'] in range(200,300):
            return agent_result
    else:
        customer_result = invoke_http(get_customer_URL, method='GET')
        if customer_result['code'] in range(200,300):
            return customer_result
        

@app.route("/profile_page", methods=['PUT'])
def update_profile():
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

def processMakeBooking(data):
    get_agent_URL = agent_URL + str(id)
    get_customer_URL = customer_URL + str(id)
    #invoke agent microservice
    if data['type'] == 'agent':
        agent_result = invoke_http(get_agent_URL, method='PUT',json=data)
        if agent_result['code'] in range(200,300):
            return agent_result
    else:
        customer_result = invoke_http(get_customer_URL, method='PUT',json=data)
        if customer_result['code'] in range(200,300):
            return customer_result

    

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5123, debug=True)
