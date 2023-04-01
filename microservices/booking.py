from flask import Flask, request, jsonify

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from os import environ
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app import app, db

class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, nullable=False)
    datetimestart = db.Column(db.DateTime,nullable=False)
    datetimeend = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(45),nullable=False)

    def __init__(self, booking_id, agent_id, customer_id, property_id, datetimestart, datetimeend, status):
        self.booking_id = booking_id
        self.agent_id = agent_id
        self.customer_id = customer_id
        self.property_id = property_id
        self.datetimestart = datetimestart
        self.datetimeend = datetimeend
        self.status = status

    def json(self):
        return {"booking_id": self.booking_id, "agent_id": self.agent_id, "customer_id": self.customer_id, "property_id": self.property_id, "datetimestart": self.datetimestart,"datetimeend":self.datetimeend, "status": self.status}

# GET BOOKING
@app.route("/booking/<booking_id>")
def get_booking(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if booking:
        return jsonify(
            {
                "code": 200,
                "data": booking.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "booking not found."
        }
    ), 404

# GET ALL OPEN BOOKINGS
@app.route("/booking/pending/")
def get_all_booking_pending():
    booking_list = Booking.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'pending': 
            booking = booking.json()
            temp.append(booking)
    if len(temp):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": temp
                }
            }
        )
    return jsonify(
        {
                "code": 200,
                "data": {
                    "books": []
                }
            }
    ), 200

# GET ALL ACCEPTED BOOKINGS
@app.route("/booking/accepted/")
def get_all_booking_accepted():
    booking_list = Booking.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'accepted': 
            booking = booking.json()
            temp.append(booking)
    if len(temp):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": temp
                }
            }
        )
    return jsonify(
        {
                "code": 200,
                "data": {
                    "books": []
                }
            }
    ), 200

#GET ALL REJECTED BOOKINGS
@app.route("/booking/rejected/")
def get_all_booking_rejected():
    booking_list = Booking.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'rejected': 
            booking = booking.json()
            temp.append(booking)
    if len(temp):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": temp
                }
            }
        )
    return jsonify(
        {
                "code": 200,
                "data": {
                    "books": []
                }
            }
    ), 200

#accept or reject a booking
@app.route("/booking/<string:booking_id>/", methods=['PUT'])
def accept_booking(booking_id):
    data = request.get_json()
    status_to_change = data['status']
    print(status_to_change)
    booking_id = int(booking_id)
    if status_to_change == 'accepted':
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if booking:
            print(booking)
            if booking.status != 'pending':
                return jsonify(
            {
                "code": 404,
                "message": "booking is not open"
            }
        ), 404
            data = request.get_json()
            booking.status = 'accepted'
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": booking.json()
                }
            )
        return jsonify(
            {
                "code": 404,
                "data": {
                    "booking_id": booking_id
                },
                "message": "booking not found"
            }
        ), 404
    
    else:
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if booking:
            if booking.status != 'pending':
                return jsonify(
            {
                "code": 404,
                "message": "booking is not open"
            }
        ), 404
            data = request.get_json()
            booking.status = 'rejected'
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": booking.json()
                }
            )
        return jsonify(
            {
                "code": 404,
                "data": {
                    "booking_id": booking_id
                },
                "message": "booking not found"
            }
        ), 404
    

#add booking
@app.route("/booking", methods=['POST'])
def create_booking():
    data = request.get_json()
    data['booking_id'] = None
    booking = Booking(**data)

    try:
        db.session.add(booking)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the booking."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": booking.json()
        }
    ), 201   

#delete booking
@app.route("/booking/<booking_id>", methods=['DELETE'])
def delete_booking(booking_id):
    booking_id = int(booking_id)
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "booking_id": booking_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "booking_id": booking_id
            },
            "message": "booking not found."
        }
    ), 404

#create event for google calendar api
@app.route("/booking/create_event", methods=['POST'])
def create_calendar_event():
    data = request.get_json()
    #example start end format {
    #"start" : "2023-03-24T09:00:00", 
    #"end" : "2023-03-24T10:00:00"
    #} 24 march 9 to 10 am
    start = data['start']
    end = data['end']
    property_name = data["property_name"]
    customer_name = data["customer_name"]

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        summary = "Booking with " + customer_name + " for " + property_name

        event = {
        'summary': summary,
        'description': summary,
        'start': {
            'dateTime': start,
            'timeZone': 'Singapore',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Singapore',
        },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(event.get('htmlLink'))
        return jsonify(
            {
                "code": 200,
                "data": "Event created" + event.get('htmlLink')
            }
        )
        # return ('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        return jsonify({
                "code": 500,
                "message": "An error occurred: " + error
            }), 500

        # return('An error occurred: %s' % error)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)






