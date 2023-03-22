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

    
class Property(db.Model):
    __tablename__ = 'property'
    property_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(45),nullable=False)
    postalcode = db.Column(db.Integer,nullable=False)
    property_type = db.Column(db.String(45),nullable=False)
    square_feet = db.Column(db.Integer,nullable=False)
    room = db.Column(db.Integer,nullable=False)
    facing = db.Column(db.String(45),nullable=False)
    build_year = db.Column(db.Integer,nullable=False)
    estimated_cost = db.Column(db.Integer,nullable=False)
    image = db.Column(db.Integer, nullable=False)
    

    def __init__(self, property_id, agent_id, customer_id, name, address, postalcode, property_type,square_feet,room,facing,build_year,estimated_cost,image):
        self.property_id = property_id
        self.agent_id = agent_id
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.postalcode = postalcode
        self.property_type = property_type
        self.square_feet = square_feet
        self.room = room
        self.facing = facing
        self.build_year = build_year
        self.estimated_cost = estimated_cost
        self.image = image

    def json(self):
        return {"property_id": self.property_id, "agent_id": self.agent_id, "customer_id":
                self.customer_id, "name": self.name, "address": self.address, "postalcode": self.postalcode, "property_type": self.property_type, "square_feet": self.square_feet, "room": self.room, "facing": self.facing, "build_year": self.build_year, "estimated_cost": self.estimated_cost, "image": self.image}


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
@app.route("/booking/pending/<person_id>")
def get_all_booking_pending(person_id):
    person_id = int(person_id)
    booking_list = Booking.query.all()
    property_list = Property.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'pending' and booking.agent_id == person_id: 
            booking = booking.json()
            for property in property_list:
                if property.property_id == booking['property_id']:
                    booking['customer_name'] = property.name 
                    booking['address'] = property.address 
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
@app.route("/booking/accepted/<person_id>",methods=['GET'])
def get_all_booking_accepted(person_id):
    person_id = int(person_id)
    booking_list = Booking.query.all()
    property_list = Property.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'accepted' and booking.agent_id == person_id: 
            booking = booking.json()
            for property in property_list:
                if property.property_id == booking['property_id']:
                    booking['customer_name'] = property.name 
                    booking['address'] = property.address 
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
@app.route("/booking/rejected/<person_id>", methods=['GET'])
def get_all_booking_rejected(person_id):
    person_id = int(person_id)
    booking_list = Booking.query.all()
    property_list = Property.query.all()
    temp = []
    for booking in booking_list:
        if booking.status == 'rejected' and booking.agent_id == person_id: 
            booking = booking.json()
            for property in property_list:
                if property.property_id == booking['property_id']:
                    booking['customer_name'] = property.name 
                    booking['address'] = property.address 
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

#Accept a booking
@app.route("/booking/booking_action/<booking_id>/<status>", methods=['PUT'])
def accept_booking(booking_id,status):
    booking_id = int(booking_id)
    if status == 'accept':
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
    booking = Booking.query.filter_by(bookind_id=booking_id).first()
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

