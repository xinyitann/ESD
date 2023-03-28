import requests
import json

# to convert postal code given by user to coordinates
def convert_postal_code_to_coordinates(postalCode):
    # Google Map API key
    apiKey = "AIzaSyDkG3Szdo9lSMTcrQvFug5-MhXmwJekgAw"

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

    # Access token for One Map API (expires every 3 days)
    # Instructions to generate a new access token is in the README.md
    accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMTAxLCJ1c2VyX2lkIjoxMDEwMSwiZW1haWwiOiJjaHVsaW50aWFuQGdtYWlsLmNvbSIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTY3OTg5MDY3MywiZXhwIjoxNjgwMzIyNjczLCJuYmYiOjE2Nzk4OTA2NzMsImp0aSI6ImU4ZDQzNTU2Yzk0ZDk0NWQyZTA2YTg3ZjM1NTFhZDQ1In0._1LweNdlw9EY_utqcNYPqReFYjK1dHe-38KI1hRWE8U"

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
    print(responseObj["GeocodeInfo"])
    for building in responseObj["GeocodeInfo"]:
        postalCodes.append(building["POSTALCODE"])
        print(building["POSTALCODE"])

    return postalCodes

searchInput = '530324'
print(list_from_postal_code_input(searchInput))