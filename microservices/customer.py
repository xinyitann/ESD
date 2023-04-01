from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@host.docker.internal:3306/property_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(20), nullable=False)

    def __init__(self, name, phone, email):
        # self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    def json(self):
        return {"customer_id": self.customer_id, "name": self.name, "phone": self.phone, "email": self.email}



# GET ONE CUSTOMER
@app.route("/customer/<string:customer_id>")
def find_customer(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "customer not found."
        }
    ), 404

# ADDING A CUSTOMER
@app.route("/customer", methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(**data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201


@app.route("/customer/<string:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        data = request.get_json()
        if data['name']:
            customer.name = data['name']
        if data['phone']:
            customer.phone = data['phone']
        if data['email']:
            customer.email = data['email'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "customer not found."
        }
    ), 404


@app.route("/customer/<string:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customer_id": customer_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "customer not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700, debug=True)
