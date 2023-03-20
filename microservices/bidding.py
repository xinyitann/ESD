from app import app,db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class Bidding(db.Model):
    __tablename__ = 'bidding'


    bidding_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    end_date = db.Column(db.TIMESTAMP, nullable=False)
    option_fee = db.Column(db.Float)
    highest_bid = db.Column(db.Float)


    def __init__(self, bidding_id, customer_id, start_date, end_date, option_fee, highest_bid):
        self.bidding_id = bidding_id
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date
        self.option_fee = option_fee
        self.highest_bid = highest_bid


    def json(self):
        return {"bidding_id": self.bidding_id, "customer_id": self.customer_id, "start_date": self.start_date, "end_date": self.end_date, "option_fee": self.option_fee, "highest_bid": self.highest_bid}

#get all bids from database
@app.route("/bidding")
def get_all():
    biddinglist = Bidding.query.all()
    if len(biddinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bids": [bid.json() for bid in biddinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bids."
        }
    ), 404

# Add new bids
@app.route("/bidding/<string:bidding_id>", methods=['POST'])
def create_bids(bidding_id):
    if (Bidding.query.filter_by(bidding_id=bidding_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "bidding_id": bidding_id
                },
                "message": "Bid already exists."
            }
        ), 400

    data = request.get_json()
    bidding = Bidding(bidding_id,**data)

    try:
        db.session.add(bidding)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "bidding_id": bidding_id
                },
                "message": "An error occurred creating the bid."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": bidding.json()
        }
    ), 201

# update existing bidding details
@app.route("/bidding/<string:bidding_id>", methods=['POST'])
def update_bids(bidding_id):
    bids = Bidding.query.filter_by(bidding_id=bidding_id).first()
    if bids:
        data = request.get_json()
        if data['customer_id']:
            bids.customer_id = data['customer_id']
        if data['start_date']:
            bids.start_date = data['start_date']
        if data['end_date']:
            bids.end_date = data['end_date'] 
        if data['option_fee']:
            bids.option_fee = data['option_fee']
        if data['highest_bid']:
            bids.highest_bid = data['highest_bid']
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
                "bidding_id": bidding_id
            },
            "message": "Bidding_id not found."
        }
    ), 404

#delete bids
@app.route("/bidding/<string:bidding_id>", methods=['DELETE'])
def delete_bid(bidding_id):
    bids = Bidding.query.filter_by(bidding_id=bidding_id).first()
    if bids:
        db.session.delete(bids)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bidding_id": bidding_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "bidding_id": bidding_id
            },
            "message": "Bidding_id not found."
        }
    ), 404




if __name__ == '__main__':
    app.run(port=5001, debug=True)