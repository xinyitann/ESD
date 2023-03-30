from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

property_URL = "http://localhost:5001/property"
agent_URL="http://localhost:5003/agent"

# validate seach input
def validate_search_input(search):
    # will have to get agent_id from agent profile somehow
    if any( c.isalnum() for c in search):
        return True
    
    else:
        return False

@app.route("/search_list/<string:search>", methods=['GET'])
def process_search(search):
    # Simple check of input format and data of the request are JSON
    # if request.is_json:
    #     try:
            # search_details = request.get_json()
            # print("\nReceived a search in JSON:", search_details)

            # Validate accept search input
    if not validate_search_input(search):
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
            "message": "Invalid accept search input: missing or invalid required fields."
        }), 400

    #check if postal code or neighbourhood
    if search.isnumeric() and len(search)==6:
        #if postal code
        print('here is property by postal code')
        print(search)
        return get_properties_from_postalcodes(search)
        

    else:
        #if neighbourhood
        print('here is property by neighbourhood')
        print(search)
        return get_properties_by_neighbourhood(search)

def get_properties_by_neighbourhood(search):
    print('\n-----Invoking property microservice for neighbourhood-----')
    # neighbourhood = "Holland"
    updated_property_URL=property_URL+'/neighbourhood/'+ search
    property_result = invoke_http(updated_property_URL,method='GET',json=None)
    print('property_result from property microservice:', property_result)

    code = property_result["code"]
    message = json.dumps(property_result)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (search error) message with routing_key=search.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="search.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nsearch status ({:d}) published to the RabbitMQ Exchange:".format(
            code), property_result)

        print("\nsearch published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"property_result": property_result},
            "message": "search creation failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "property_result": property_result,
    }
}

#Get properties from list of postal codes 
def get_properties_from_postalcodes(postalcode):
    postalcode_list=list_from_postal_code_input(postalcode)
    postalcode_str=str(postalcode_list)
    print(postalcode_str)
    # print(postalcode_list) #['530321', '530323', '530325', '530320', '530324', '530322', '530322', '530326', '530333', '530332']

    # if  postalcode_list:
    #     for postalcode in postalcode_list:
    #       print(postalcode)
    print('\n-----Invoking property microservice for postalcode-----')
    updated_property_URL=property_URL+'/postal_code/'+ postalcode_str
    property_result = invoke_http(updated_property_URL,method='GET',json=None)
    print('property_result from property microservice:', property_result)

    code = property_result["code"]
    message = json.dumps(property_result)
    print(message)
    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (search error) message with routing_key=search.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="search.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nsearch status ({:d}) published to the RabbitMQ Exchange:".format(
            code), property_result)

        print("\nsearch published to RabbitMQ Exchange.\n")\


        return {
            "code": 500,
            "data": {"property_result": property_result},
            "message": "search creation failure sent for error handling."
        }

    return {
    "code": 201,
    "data": {
        "property_result": property_result,
    }
}
    # else:
    #     print("line 166")


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
    print(response_json)
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
    print(lat)

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

# searchInput = '530324'
# print(list_from_postal_code_input(searchInput))

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for searching...")
    app.run(host="0.0.0.0", port=5106, debug=True)