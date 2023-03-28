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
bid_URL = "http://localhost:5500/bids"
auction_URL = "http://localhost:5002/auctions"
customer_URL = "http://localhost:5700/customer"

def validate_bid_input(bid_details):
    # NEED TO CHANGE 
    required_fields = ['auction_id', 'customer_id', 'bid_amount', 'property_id']

    for field in required_fields:
        if field not in bid_details:
            return False
    return True

@app.route("/make_bid", methods=['POST'])
def make_bidding():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            bid_details = request.get_json()
            print("\nReceived a bidding listing in JSON:", bid_details)

            # Validate bidding input
            if not validate_bid_input(bid_details):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid listing input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (listing input error) message with routing_key=bidding.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error",
                                                 body=json.dumps(error_message),
                                                 properties=pika.BasicProperties(delivery_mode=2))
                print("\nInvalid listing input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid bidding input: missing or invalid required fields."
                }), 400

            property_id = bid_details["property_id"]
            # get the auction_id from the property microservice 
            auction_result = get_auction_id(property_id)
            
            if auction_result['code'] == 201:
                print("auction_id", auction_result['data']["auction_result"]["data"])
                auction_id = auction_result["data"]['auction_result']["data"]

                print("bid_details ", bid_details)


                # check if the bid amount is more than the starting price

                starting_price_result = get_starting_price(auction_id)

                starting_price = starting_price_result['data']["starting_price_result"]["data"]

                if bid_details["bid_amount"] > starting_price:
                    if "bid_id" in bid_details:
                        # if bid id is found in bid details means that the bid needs to be updated
                        bidding_details = {
                            "bid_id" : bid_details["bid_id"],
                            "customer_id": bid_details["customer_id"],
                            "auction_id": str(auction_id),
                            "bid_amount": bid_details["bid_amount"]
                        }

                        highest_bidder= processUpdateBidding(bidding_details) # would get back the highest bid and the customer_id
                        print('\nbidding_details: ', highest_bidder)
                    
                    else:
                        # if there is no bid id then the bid needs to be created
                        bidding_details = {
                            "customer_id": bid_details["customer_id"],
                            "auction_id": auction_id,
                            "bid_amount": bid_details["bid_amount"]
                        }

                        print("bidding_details ", bidding_details)
                        highest_bidder = processAddBidding(bidding_details) # would get back the highest bid and the customer_id
                        print('\nbidding_details: ', highest_bidder)
                    

                    # update the highest bid in the auction microservice and return the highest bid details back to the UI
                    highest_bid = {
                            "highest_bid" : highest_bidder["data"]["highest_bidder"]["data"]["highest_bid"],
                            "customer_id": highest_bidder["data"]["highest_bidder"]["data"]["customer_id"],
                            "auction_id": str(auction_id),
                        }
                    highest_bidder_auction = processUpdateHighestBidder(highest_bid)

                    print('\n------------------------')
                    print('\nauction_result: ', auction_result)
                    print('\nhighest_bidder_auction: ', highest_bidder_auction)
                    return jsonify(highest_bidder_auction), highest_bidder_auction["code"]

                else:
                    error_message = {
                    "code": 400,
                    "message": "Bid amount is lesser than the starting price."
                    }
                    print('\n\n-----Publishing the (listing input error) message with routing_key=bidding.error-----')
                    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error",
                                                    body=json.dumps(error_message),
                                                    properties=pika.BasicProperties(delivery_mode=2))
                    print("\nInvalid listing input published to the RabbitMQ Exchange.\n")

                    return jsonify({
                        "code": 400,
                        "message": "Bid amount is lesser than the starting price."
                    }), 400

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "make_bid.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/close_bidding", methods=['POST'])
def close_bidding_period():
    print("closing the bid step 10 onwards in the microservice interaction diagram")
    # update the auction microservice to close the bidding period
    # return the highest bidder customer_id
    # call the customer microservice to get the customer name and email
    # call the notification.py to send the notification to the wining customer 


@app.route("/make_payment", methods=['POST'])
def make_payment():
    print("user will make payment here")
    # call the external service provider when customer want to make payment 


def get_auction_id(property_id):
    print('\n-----Invoking property microservice-----')
    auction_id_URL = property_URL + "/auction/" + str(property_id)
    auction_result = invoke_http(auction_id_URL, method='GET', json=None)
    print('auction_result from property microservice:', auction_result)


    code = auction_result["code"]
    message = json.dumps(auction_result)


    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nbidding status ({:d}) published to the RabbitMQ Exchange:".format(
            code), auction_result)

        print("\nbidding published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"auction_result": auction_result},
            "message": "booking creation failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "auction_result": auction_result,
    }
}


def get_starting_price(auction_id):
    print('\n-----Invoking property microservice-----')
    starting_price_URL = auction_URL + "/starting_price/" + str(auction_id)
    starting_price_result = invoke_http(starting_price_URL, method='GET', json=None)
    print('starting_price_result from property microservice:', starting_price_result)


    code = starting_price_result["code"]
    message = json.dumps(starting_price_result)


    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (booking error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nbidding status ({:d}) published to the RabbitMQ Exchange:".format(
            code), starting_price_result)

        print("\nbidding published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"starting_price_result": starting_price_result},
            "message": "getting auction starting price failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "starting_price_result": starting_price_result,
    }
}




def processAddBidding(bidding_details):
    print('\n-----Invoking bid microservice-----')
    auction_id = str(bidding_details["auction_id"])
    add_bidding_URL = bid_URL + "/" + auction_id + "/" + str(bidding_details["customer_id"])
    bidding_details = invoke_http(add_bidding_URL, method='POST', json=bidding_details)
    print('bidding_details from bid microservice:', bidding_details)

    code = bidding_details["code"]
    message = json.dumps(bidding_details)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (property error) message with routing_key=property.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bidding_details)

        print("\nauction published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"bidding_details": bidding_details},
            "message": "auction creation failure sent for error handling."
        }
    
    else:
        # get the highest bid after adding the bid details 
        print('\n-----Invoking bid microservice for highest bid-----')
        get_highest_bid_URL = bid_URL + "/highest_bid/" +  auction_id
        print("get_highest_bid_URL " , get_highest_bid_URL)
        highest_bidder = invoke_http(get_highest_bid_URL, method='GET', json=None)
        print('highest_bidder from bid microservice:', highest_bidder)

        if code not in range(200, 300):
            # Inform the error microservice
            print('\n\n-----Publishing the (property error) message with routing_key=property.error-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
            print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
                code), highest_bidder)

            print("\nauction published to RabbitMQ Exchange.\n")\

            return {
                "code": 500,
                "data": {"highest_bidder": highest_bidder},
                "message": "auction creation failure sent for error handling."
            }


    return {
    "code": 201,
    "data": {
        "highest_bidder": highest_bidder,
    }
}


def processUpdateBidding(bidding_details):
    print('\n-----Invoking bid microservice-----')
    auction_id = str(bidding_details["auction_id"])
    add_bidding_URL = bid_URL + "/" + str(bidding_details["bid_id"]) + "/" + str(bidding_details["customer_id"]) + "/" + auction_id
    bidding_details = invoke_http(add_bidding_URL, method='PUT', json=bidding_details)
    print('auction_result from bid microservice:', bidding_details)

    code = bidding_details["code"]
    message = json.dumps(bidding_details)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (bidding error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bidding_details)

        print("\nauction published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"bidding_details": bidding_details},
            "message": "auction creation failure sent for error handling."
        }
    else:
        # get the highest bid after updating the bid details 
        print('\n-----Invoking bid microservice-----')
        get_highest_bid_URL = bid_URL + "/highest_bid/" + auction_id
        highest_bidder = invoke_http(get_highest_bid_URL, method='GET', json=None)
        print('auction_result from bid microservice:', highest_bidder)

        if code not in range(200, 300):
            # Inform the error microservice
            print('\n\n-----Publishing the (bidding error) message with routing_key=bidding.error-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
            print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
                code), highest_bidder)

            print("\nauction published to RabbitMQ Exchange.\n")\

            return {
                "code": 500,
                "data": {"highest_bidder": highest_bidder},
                "message": "auction creation failure sent for error handling."
            }


    return {
    "code": 201,
    "data": {
        "highest_bidder": highest_bidder,
    }
}




def processUpdateHighestBidder(highest_bidder):
    print("update the highest bidder details in auction microservice")

    print('\n-----Invoking auction microservice-----')
    auction_id = str(highest_bidder["auction_id"])
    update_auction_URL = auction_URL + "/highest_bid/" + auction_id
    update_highest_bid = invoke_http(update_auction_URL, method='PUT', json=highest_bidder)
    print('update_highest_bid from auction microservice:', update_highest_bid)

    code = update_highest_bid["code"]
    message = json.dumps(update_highest_bid)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (bidding error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nauction status ({:d}) published to the RabbitMQ Exchange:".format(
            code), update_highest_bid)

        print("\nauction published to RabbitMQ Exchange.\n")\

        return {
            "code": 500,
            "data": {"bidding_details": update_highest_bid},
            "message": "auction creation failure sent for error handling."
        }


    return {
    "code": 201,
    "data": {
        "highest_bidder": highest_bidder,
    }
}



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for adding a making bid...")
    app.run(host="0.0.0.0", port=5900, debug=True)
