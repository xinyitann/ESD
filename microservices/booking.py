from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/property_management'
#environ.get('dbURL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)



class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(45),nullable=False)

    def __init__(self, booking_id, agent_id, customer_id, property_id, datetime, status):
        self.booking_id = booking_id
        self.agent_id = agent_id
        self.customer_id = customer_id
        self.property_id = property_id
        self.datetime = self.datetime
        self.status = self.status

    def json(self):
        return {"booking_id": self.booking_id, "agent_id": self.agent_id, "customer_id": self.customer_id, "property_id": self.property_id, "datetime": self.datetime, "status": self.status}

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
            "code": 404,
            "message": "There are no open bookings"
        }
    ), 404

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
            "code": 404,
            "message": "There are no open bookings"
        }
    ), 404

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
            "code": 404,
            "message": "There are no open bookings"
        }
    ), 404

#accept or reject a booking
@app.route("/booking/<booking_id>/<status_to_change>", methods=['PUT'])
def accept_booking(booking_id,status_to_change):
    booking_id = int(booking_id)
    if status_to_change == 'accepted':
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

#add booking
@app.route("/booking/<booking_id>", methods=['POST'])
def add_booking(booking_id):
    booking = Booking.query.filter_by(bookind_id=booking_id).first()
    if not booking:
        db.session.add(booking)
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
            "message": "booking already exists"
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


