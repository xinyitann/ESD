from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika

import requests
import json
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

property_URL = "http://localhost:5001/property"
agent_URL="http://localhost:5003/agent"

# search_input='530321'
def validate_search_input(search_input):
    # will have to get agent_id from agent profile somehow

    if len(search_input)==6 and search_input.isdigit():
        #if postal code
        # return convert_postal_code_to_coordinates(search_input)
        print('here is property by postal code')

    else:
        #if neighbourhood
        print('here is property by neighbourhood')
    
@app.route("/search_list",methods=['GET']) 
def get_property_by_neighbourhood():

    if request.is_json:
        try:
            search_details = request.get_json()
            print("\nReceived a search in JSON:", search_details)

            # Validate search input
            if not validate_search_input(search_details):
                # Inform the error microservice
                error_message = {
                    "code": 400,
                    "message": "Invalid accept search input: missing or invalid required fields."
                }
                print('\n\n-----Publishing the (search input error) message with routing_key=search.error-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="search.error", 
                        body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2)) 
                print("\nInvalid search input published to the RabbitMQ Exchange.\n")

                return jsonify({
                    "code": 400,
                    "message": "Invalid search input: missing or invalid required fields."
                }), 400

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "search.py internal error: " + ex_str
            }), 500


    print('\n-----Invoking property microservice-----')
    neighbourhood = "Holland"
    updated_property_URL=property_URL+'/'+ neighbourhood
    property_result = invoke_http(updated_property_URL,method='GET',json=None)
    print('property_result from property microservice:', property_result)

    # code = property_result["code"]
    # message = json.dumps(property_result)


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
        




# to convert postal code given by user to coordinates
def convert_postal_code_to_coordinates(postalCode):

    # Google Map API key
    apiKey = os.getenv('GOOGLE_MAPS_API_KEY')

    # Example API endpoint to geocode the postal code
    apiEndpoint = f"https://maps.googleapis.com/maps/api/geocode/json?address={postalCode}&key={apiKey}"

    # Send a GET request to the API endpoint
    response = requests.get(apiEndpoint)

    # Parse the JSON response
    response_json = response.json()

    # Extract the latitude and longitude coordinates from the response
    latitude = response_json['results'][0]['geometry']['location']['lat']
    longitude = response_json['results'][0]['geometry']['location']['lng']

    return [latitude, longitude]

# To convert coordinates to SVY21 format
def convert_coordinates_to_SVY21(lat, long):

    apiEndpoint= f"https://developers.onemap.sg/commonapi/convert/4326to3414?latitude={lat}&longitude={long}"

    # Send a GET request to the API endpoint
    response = requests.get(apiEndpoint)

    # Convert response.content to JSON
    jsonString = response.content.decode('utf8').replace("'", '"')
    jsonObj = json.loads(jsonString)

    # Organise data in required format
    return str(jsonObj["X"]) + "," + str(jsonObj["Y"])



# Get a list of HDBs from a postal code input
def list_from_postal_code_input(searchInput):

    # OneMap API, regenerate access token and change it in .env file
    accessToken = os.getenv('ONE_MAP_API_KEY')

    # Convert searched postal code to lat and long
    lat, long = convert_postal_code_to_coordinates(searchInput)

    # Convert lat and long to required SVY21 format
    location = convert_coordinates_to_SVY21(lat, long)

    apiEndpoint = f"https://developers.onemap.sg/privateapi/commonsvc/revgeocodexy?location={location}&token={accessToken}?&buffer=500&addressType=HDB"

    # Send a GET request to the API endpoint
    response = requests.get(apiEndpoint)

    # Convert response.content to JSON
    responseString = response.content.decode('utf8').replace("'", '"')
    responseObj = json.loads(responseString)

    # Get list of postal codes from json obj
    postalCodes = []
    for building in responseObj["GeocodeInfo"]:
        postalCodes.append(building["POSTALCODE"])

    return postalCodes

# print(list_from_postal_code_input(searchInput))

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for searching...")
    app.run(host="0.0.0.0", port=5105, debug=True)