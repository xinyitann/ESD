from app import app, db
from flask import Flask, request, jsonify
import mysql.connector
import base64
from PIL import Image
import io
import PIL  
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
from agent import Agent
from customer import Customer
from auctionService import AuctionService
import os


class Property(db.Model):
    __tablename__ = 'property'

    property_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.agent_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    postalcode = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(45), nullable=False)
    square_feet = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    facing = db.Column(db.String(45), nullable=False)
    build_year = db.Column(db.Integer, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)
    neighbourhood = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String, nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.auction_id'), nullable=False)

    def __init__(self, agent_id, customer_id, name, address, postalcode, property_type, square_feet, room, facing, build_year, estimated_cost, neighbourhood,image,auction_id):
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
        self.neighbourhood = neighbourhood
        self.image = image
        self.auction_id = auction_id

    def json(self):
        return {"property_id": self.property_id, "agent_id": self.agent_id, "customer_id": self.customer_id, "name": self.name, "address": self.address, "postalcode": self.postalcode, "property_type": self.property_type, "square_feet": self.square_feet, "room": self.room, "facing": self.facing, "build_year": self.build_year, "estimated_cost": self.estimated_cost, "neighbourhood":self.neighbourhood,"image": self.image, "auction_id":self.auction_id}
    
    def json_without_image(self):
        return {"property_id": self.property_id, "agent_id": self.agent_id, "customer_id": self.customer_id, "name": self.name, "address": self.address, "postalcode": self.postalcode, "property_type": self.property_type, "square_feet": self.square_feet, "room": self.room, "facing": self.facing, "build_year": self.build_year, "estimated_cost": self.estimated_cost, "neighbourhood":self.neighbourhood,"image": self.image, "auction_id":self.auction_id}

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

#function works
@app.route("/property/neighbourhood/<string:neighbourhood>",methods=['GET'])
def get_property_by_neighbourhood(neighbourhood):
    prop_list = Property.query.filter_by(neighbourhood=neighbourhood).all()

    if prop_list:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "properties": [property.json() for property in prop_list]
                }
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "No properties found for the specified neighbourhood."
            }
        ), 404

#function working
@app.route("/property/postal_code/<string:postalcode_str>",methods=['GET'])
def get_property_by_postalcode(postalcode_str):

    # print(postalcode_str)
    # print(type(postalcode_str)) #string

    #convert string to list 
    postalcode_list=eval(postalcode_str)
    # print(postalcode_list)
    # print(type(postalcode_list)) #list

    postal_list=[]
    for postalcode in postalcode_list:  
        # print(postalcode)
        prop_list = Property.query.filter_by(postalcode=postalcode).all()
        # print(prop_list)
        if prop_list:
            postal_list.append(prop_list)
        else:
            print("stupid")
    # for query in postal_list:
    #     print(str(query))

    # print(postal_list)
    if postal_list:
        print("hello")
        return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "properties": [property.json() for query in postal_list for property in query]
                            #[word for sentence in text for word in sentence]

                        }
                    }
                )
    return jsonify(
        {
            "code": 404,
            "message": "Property not found."
        }
), 404


# if you dont put string default it is string (so for other variable types you need to put)
@app.route("/property/<property_id>")
def find_by_property_id(property_id):
    # get the specific property (.first --> gets us the property if we dont have it we will get the list of property)
    property_id = int(property_id)
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

@app.route("/property/agent/<agent_id>")
def find_by_agent_id(agent_id):
    # get the specific property (.first --> gets us the property if we dont have it we will get the list of property)
    agent_id = int(agent_id)
    property_list = Property.query.all()
    temp = []
    for item in property_list:
        if item.agent_id == agent_id:
            temp.append(item.json())
    return jsonify(
        {
            "code": 200,
            "data": temp
        }
    ), 200

@app.route("/property/details/<property_id>")
def find_by_property_id_no_image(property_id):
    # get the specific property (.first --> gets us the property if we dont have it we will get the list of property)
    property_id = int(property_id)
    property = Property.query.filter_by(property_id=property_id).first()
    if property:
        return jsonify(
            {
                "code": 200,
                "data": property.json_without_image()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Property not found."
        }
    ), 404

# by default it is GET (for other methods you need to specify)
@app.route("/property", methods=['POST'])
def create_property():
    data = request.get_json()
    
    # Add print statements to check the data
    # print("Data:", data)
    # print("Agent ID:", data['agent_id'])
    # print("Customer ID:", data['customer_id'])
    # print(store_image(data['image']))
    
    property = Property(
        auction_id=data['auction_id'],
        agent_id=data['agent_id'],
        customer_id=data['customer_id'],
        name=data['name'],
        address=data['address'],
        postalcode=data['postalcode'],
        property_type=data['property_type'],
        square_feet=data['square_feet'],
        room=data['room'],
        facing=data['facing'],
        build_year=data['build_year'],
        estimated_cost=data['estimated_cost'],
        image=data['image'],
        neighbourhood=data['neighbourhood']
    )


    try:
        db.session.add(property)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the property. " + str(e)
            }
        ), 500

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
        property.neighbourhood = data['neighbourhood']

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

@app.route("/property/auction/<string:property_id>",methods=['GET'])
def get_auction(property_id):
    property = Property.query.filter_by(property_id=property_id).first()
    # print(property)
    list = property.json_without_image()
    
    if property:
        return jsonify(
            {
                "code": 200,
                "data": list["auction_id"]
                    
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Auction not found."
        }
    ), 404

@app.route("/property/name/<int:auction_id>", methods=['GET'])
def get_property_name(auction_id):
    # filter properties by auction_id
    property = Property.query.filter_by(auction_id=auction_id).first()
    if property:
        # return the name of the property
        return jsonify(
            {
                "code": 200,
                "data": {
                    "property_name": property.name
                }
            }
        )
    # if property not found return 404
    return jsonify(
        {
            "code": 404,
            "message": "Property not found with auction_id: {}".format(auction_id)
        }
    ), 404

# get property info using customer id
@app.route("/property/details/customer/<string:customer_id>")
def find_property_info_using_customerid(customer_id):
    property = Property.query.filter_by(customer_id=customer_id).first()
    if property:
        return jsonify(
            {
                "code": 200,
                "data": property.json_without_image()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Property not found."
        }
    ), 404

# get property using auction_id
@app.route("/property/details/auction/<int:auction_id>", methods=['GET'])
def get_property_from_auction(auction_id):
    # filter properties by auction_id
    property = Property.query.filter_by(auction_id=auction_id).first()
    if property:
        # return the name of the property
        return jsonify(
            {
                "code": 200,
                "data": {
                    "property": property.json()
                }
            }
        )
    # if property not found return 404
    return jsonify(
        {
            "code": 404,
            "message": "Property not found with auction_id: {}".format(auction_id)
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) # so that it can be accessed from outside 
