from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

agent_URL = environ.get('agent_URL') or "http://localhost:5003/agent"
customer_URL = environ.get('customer_URL') or "http://localhost:5700/customer"



@app.route("/login/<email>", methods=['GET'])
def login(email):
    if True:
        try:
            result = processMakeBooking(email)
            return jsonify(result), result['code']
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "login.py internal error: " + ex_str
            }), 500

def processMakeBooking(email):

    get_agent_URL = agent_URL + "/get_id_by_email/" + email
    print(get_agent_URL)
    get_customer_URL = customer_URL + "/get_id_by_email/" + email

    #invoke agent microservice
    agent_result = invoke_http(get_agent_URL, method='GET')
    print('agent result:', agent_result)

    #invoke customer microservice
    customer_result = invoke_http(get_customer_URL, method='GET')
    print('customer result:', customer_result)
 
    if agent_result['code'] not in range(200,300) and customer_result['code'] not in range(200,300):
        result = {}
        result['code'] = 404
        return result

    elif agent_result['code'] in range(200,300):
        result = {}
        result['code'] = 200
        result['id'] = agent_result['data']['agent_id']
        result['user_type'] = 'agent'
        return result
    
    else:
        result = {}
        result['code'] = 200
        result['id'] = customer_result['data']['customer_id']
        result['user_type'] = 'user'
        return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5805, debug=True)
