from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ


app = Flask(__name__)

# change the database name
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') #prepare the code for containerisation 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/property_management'
# suppress the warning messages
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# name it the same as your table name --> same for all your other microservices


class Property(db.Model):
    # database name --> what you created in your database
    __tablename__ = 'property'

    # mirror the database columns --> the data types might not correspond but its the same
    property_id=db.Column(db.Integer, nullable=False, primary_key=True)
    agent_id=db.Column(db.Integer, nullable=False)
    customer_id=db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(32),nullable=False)
    address=db.Column(db.String(45),nullable=False)
    postalcode=db.Column(db.Integer,nullable=False)
    property_type=db.Column(db.String(45),nullable=False)
    square_feet=db.Column(db.Integer, nullable=False)
    room=db.Column(db.Integer, nullable=False)
    facing=db.Column(db.String(45),nullable=False)
    build_year=db.Column(db.Integer, nullable=False)
    estimated_cost=db.Column(db.Float(53), nullable=False)
    image=db.Column(db.String(50), nullable=False)


    # constructor
    def __init__(self, property_id, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, image):
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


    # return the JSON representation of your property record
    def json(self):
        return {"property_id": self.property_id, "agent_id": self.agent_id, "customer_id":
                self.customer_id, "name": self.name, "address": self.address, "postalcode": self.postalcode, "property_type": self.property_type, "square_feet": self.square_feet, "room": self.room, "facing": self.facing, "build_year": self.build_year, "estimated_cost": self.estimated_cost, "image": self.image}


@app.route("/property")
def get_all():
    # get all the properties (same as your sql select statement)
    propertylist = Property.query.all()
    if len(propertylist):
        # format to json and return all the propertys to the calling application
        return jsonify(
            {
                "code": 200,
                "data": {
                    "properties": [property.json() for property in propertylist]
                }
            }
        )
    # the error message
    return jsonify(
        {
            "code": 404,
            "message": "There are no properties."
        }
    ), 404  # the HTTP status code (by default its 200)


# if you dont put string default it is string (so for other variable types you need to put)
@app.route("/property/<string:property_id>")
def find_by_property_id(property_id):
    # get the specific property (.first --> gets us the property if we dont have it we will get the list of property)
    property = Property.query.filter_by(property_id=property_id).first()
    if property:
        return jsonify(
            {
                "code": 200,
                "data": property.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Property not found."
        }
    ), 404


# by default it is GET (for other methods you need to specify)
@app.route("/property/<string:property_id>", methods=['POST'])
def create_property(property_id):
    # check if the property exist
    if (Property.query.filter_by(property_id=property_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "property_id": property_id
                },
                "message": "Property already exists."
            }
        ), 400

    # will get the body part of your request
    data = request.get_json()
    # it will create the property object (**data --> get the data from the body)
    # your table must match or you must check
    property = Property(property_id, **data)

    # try to commit the property first
    try:
        db.session.add(property)
        # same as your sql insert statement
        db.session.commit()

    # if it does not work it will throw an error
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "property_id": property_id
                },
                "message": "An error occurred creating the property."
            }
        ), 500

    # else it will show that it created successfully
    return jsonify(
        {
            "code": 201,
            "data": property.json()
        }
    ), 201

# create a put function


@app.route("/property/<string:property_id>", methods=['PUT'])
def update_property(property_id):
    # check if the property exist
    if(Property.query.filter_by(property_id=property_id).first()):
        # get the data
        data = request.get_json()
        print('gere')
        print(data)
        # create a property obj
        property = Property.query.filter_by(property_id=property_id).first()
        print(property.price)
        property.agent_id = data['agent_id']
        property.customer_id = data['customer_id']
        property.name = data['name']
        property.address = data['address']
        property.postalcode = data['postalcode']
        property.property_type = data['property_type']
        property.square_feet = data['square_feet']
        property.room = data['room']
        property.facing = data['facing']
        property.build_year = data['build_year']
        property.estimated_cost = data['estimated_cost']
        property.image = data['image']

        try:
            # update the property record
            db.session.commit()
        except:
            # if something went wrong return this message
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "property_id": property_id
                    },
                    "message": "An error occurred creating the property."
                }
            ), 500

        # else return that it is successful
        return jsonify(
            {
                "code": 201,
                "data": property.json()
            }
        ), 201

    else:
        # if property cannot be found return 404
        return jsonify(
            {
                "code": 404,
                "message": "Property not found."
            }
        ), 404

# create a delete function


@app.route('/property/<string:property_id>', methods=['DELETE'])
def delete_property(property_id):
 # check if the property exist
    if(Property.query.filter_by(property_id=property_id).first()):
        try:
            # get the property
            property = Property.query.filter_by(property_id=property_id).first()
            # delete the property
            db.session.delete(property)
            db.session.commit()
        except:
            # if something went wrong return this message
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "property_id": property_id
                    },
                    "message": "An error occurred creating the property."
                }
            ), 500

        # else return that it is successful
        return jsonify(
            {
                "code": 201,
                "data": property.json()
            }
        ), 201

    else:
        # if property cannot be found return 404
        return jsonify(
            {
                "code": 404,
                "message": "Property not found."
            }
        ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # so that it can be accessed from outside 
