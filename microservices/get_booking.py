from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

booking_URL = environ.get('booking_URL') or "http://localhost:5005/booking"
property_URL = environ.get('property_URL') or "http://localhost:5001/property"
customer_URL = environ.get('customer_URL') or "http://localhost:5700/customer"


@app.route("/get_booking/<agent_id>")
def get_page_info(agent_id):
    data = {}
    data['agent_id'] = int(agent_id)
    if True:
        try:
            result = processGetData(data)
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
    
def processGetData(data):
    booking_info_pending = booking_URL + "/pending/"
    booking_info_accepted = booking_URL + "/accepted/"
    booking_info_rejected = booking_URL + "/rejected/"

    agent_id = data['agent_id']

    pending_result = invoke_http(booking_info_pending, method='GET')
    if pending_result['code'] not in range(200,300):
        return pending_result
    final_pending_list = []
    pending_list = pending_result['data']['books']
    for pending in pending_list:
        if pending['agent_id'] == agent_id:
            final_pending_list.append(pending)

    accepted_result = invoke_http(booking_info_accepted, method='GET')
    if accepted_result['code'] not in range(200,300):
        return accepted_result
    final_accepted_list = []
    accepted_list = accepted_result['data']['books']
    for accepted in accepted_list:
        if accepted['agent_id'] == agent_id:
            final_accepted_list.append(accepted)

    rejected_result = invoke_http(booking_info_rejected, method='GET')
    if rejected_result['code'] not in range(200,300):
        return rejected_result
    final_rejected_list = []
    rejected_list = rejected_result['data']['books']
    for rejected in rejected_list:
        if rejected['agent_id'] == agent_id:
            final_rejected_list.append(rejected)
    
    ans_dic = {}
    ans_dic['pending'] = final_pending_list
    ans_dic['accepted'] = final_accepted_list
    ans_dic['rejected'] = final_rejected_list
    ans_dic['code'] = 200
    return ans_dic

@app.route("/get_booking_extra_info/<customer_id>")  
def get_info(customer_id):
    if True:
        try:
            result = ProcessData(customer_id)
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
                "message": "accept_booking.py internal error: " + ex_str
            }), 500
    

def ProcessData(customer_id):
    customer_info = customer_URL + customer_id
    property_info = property_URL + "/details/" + customer_id
    customer_result = invoke_http(customer_info, method='GET')
    property_result = invoke_http(property_info, method='GET')
    print(customer_result)
    print(property_result)
    dic = {}
    dic['customer_name'] = customer_result['data']['name']
    dic['address'] = property_result['data']['address']
    dic['code'] = 200
    return dic

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting booking...")
    app.run(host="0.0.0.0", port=5102, debug=True)
