from flask import Flask, request, jsonify
from datetime import datetime
import time
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@host.docker.internal:3306/property_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Bids(db.Model):
    __tablename__ = 'bids'

    bid_id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.auction_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    bid_amount = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)

    def __init__(self, auction_id, customer_id, bid_amount, created_at, updated_at):
        self.auction_id = auction_id
        self.customer_id = customer_id
        self.bid_amount = bid_amount
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self):
        return {"bid_id": self.bid_id, "auction_id": self.auction_id, "customer_id": self.customer_id, "bid_amount": self.bid_amount, "created_at": self.created_at, "updated_at": self.updated_at}


# GET BIDS
@app.route("/bids")
def find_bids():
    bids = Bids.query.all()
    if len(bids):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "properties": [bid.json() for bid in bids]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bids."
        }
    ), 404

# get one bid
@app.route("/bids/<string:bid_id>")
def get_one_bid(bid_id):
    bids = Bids.query.filter_by(bid_id=bid_id).first()
    if bids:
        return jsonify(
            {
                "code": 200,
                "data": bids.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "bid not found."
        }
    ), 404

# CREATE A BID
@app.route("/bids/<string:auction_id>/<string:customer_id>", methods=['POST'])
def create_bid(auction_id, customer_id):
    data = request.get_json()
    
    bids = Bids(
        auction_id=auction_id,
        customer_id=customer_id,
        bid_amount=data['bid_amount'],
        created_at=time.strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=time.strftime('%Y-%m-%d %H:%M:%S')
    )

    try:
        
        db.session.add(bids)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the bid."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": bids.json()
        }
    ), 201

# UPDATE BIDS
@app.route("/bids/<string:bid_id>", methods=['PUT'])
def update_bid(bid_id):
    bids = Bids.query.filter_by(bid_id=bid_id).first()
    if bids:
        data = request.get_json()
        if data['bid_amount']:
            bids.bid_amount = data['bid_amount']
            bids.updated_at = time.strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": bids.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "bid_id": bid_id
            },
            "message": "bid not found."
        }
    ), 404

# DELETE BIDS
@app.route("/bids/<string:bid_id>", methods=['DELETE'])
def delete_bid(bid_id):
    bids = Bids.query.filter_by(bid_id=bid_id).first()
    if bids:
        db.session.delete(bids)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bid_id": bid_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": bid_id
            },
            "message": "bid not found."
        }
    ), 404


# GET HIGHEST BID
@app.route("/bids/highest_bid/<string:auction_id>")
def get_highest_bid(auction_id):
    bids_list = Bids.query.filter_by(auction_id=auction_id)
    highest = 0
    for bids in bids_list:
        customer_id = bids.customer_id
        if bids.bid_amount > highest:
            highest = bids.bid_amount
    
    if highest != 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "highest_bid": highest,
                    "customer_id" : customer_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There was an error getting the highest bid"
        }
    ), 404

# check if customer has bid before
@app.route("/bids/<string:auction_id>/<string:customer_id>")
def check_user_bided(auction_id, customer_id):
    auction = Bids.query.filter_by(auction_id=auction_id, customer_id=customer_id).first()

    if auction:
        print("true")
        return jsonify(
            {
                "code": 200,
                "data": True
            }
        )
    else:
        print("false")
        return jsonify(
            {
                "code": 200,
                "data": False
            }
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
