from app import app,db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
import customer
from os import environ


class AuctionService(db.Model):
    __tablename__ = 'auctions'
        
    auction_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    starting_price = db.Column(db.Float)
    option_fee = db.Column(db.Float)
    highest_bid = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP, nullable=False,server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False,server_default=func.now())
    status = db.Column(db.String(20), nullable=False)


    def __init__(self, starting_price,option_fee, customer_id, status):
        self.starting_price = starting_price
        self.option_fee = option_fee
        self.auctions = []
        self.customer_id = customer_id
        self.status = status
    
    def json(self):
        return {"auction_id": self.auction_id, "starting_price": self.starting_price,"option_fee": self.option_fee, "highest_bid": self.highest_bid, "created_at": self.created_at, "updated_at": self.updated_at, "customer_id": self.customer_id, "status": self.status}



#Get the list of auctions
@app.route("/auctions", methods=['GET'])
def get_auctions():
    auctionList = AuctionService.query.all()

    if len(auctionList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "auctions": [auctions.json() for auctions in auctionList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no auctions."
        }
    ), 404


# Add new auction
@app.route("/auctions", methods=['POST'])
def create_auction():
    # create new auction record in database with given parameters
    data = request.get_json()
    auctions = AuctionService(
        status = data['status'],
        starting_price = data['starting_price'],
        option_fee = data['option_fee']
    )
        
    try:
        db.session.add(auctions)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the auction."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": auctions.json()

        }  
    ), 201

@app.route("/auctions/<string:auction_id>", methods=['PUT'])
def update_auction(auction_id):
    # update the auction record in the database with the given parameters
    #retrieve the new data from the request body
    #auction_update = request.get_json()
    
    auctions = AuctionService.query.filter_by(auction_id=auction_id).first()
    if(auctions):
        # get the data
        data = request.get_json()
        print(data)

        if data['auction_id']:
            auctions.auction_id = data['auction_id']
        if data['start_time']:
            auctions.start_time = data['start_time']
        if data['end_time']:
            auctions.end_time = data['end_time']
        if data['starting_price']:
            auctions.starting_price = data['starting_price']
        if data['option_fee']:
            auctions.option_fee = data['option_fee']
        if data['highest_bid']:
            auctions.highest_bid = data['highest_bid']
        if data['created_at']:
            auctions.created_at = data['created_at']
        if data['updated_at']:
            auctions.updated_at = data['updated_at']

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": auctions.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "auction_id": auction_id
            },
            "message": "Auction not found."
        }
    ), 404

@app.route('/auctions/<string:auction_id>/close', methods=['PUT'])
def close_auction(auction_id):
    print("heree")
    auction = AuctionService.query.filter_by(auction_id=auction_id).first()

    print("auction", auction)
    if auction:
        data = request.get_json()
        print("data ", data)
        if data['status']:
            auction.status = "close"
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": auction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "auction_id": auction_id
            },
            "message": "auction not found."
        }
    ), 404

    # current_time = datetime.datetime.utcnow()
    # if auction is None:
    #     return jsonify({'error': 'Auction not found'}), 404
    # if current_time < auction.start_time:
    #     return jsonify({'error': 'Auction have not started'}), 400
    # if current_time < auction.end_time :
    #     return jsonify({'message': 'Auction still ongoing'}), 200
    # if current_time > auction.end_time:
    #     return jsonify({'error': 'Auction has ended'}), 400
    # auction.end_time = current_time
    # db.session.commit()
    # return jsonify({'message': 'Auction closed successfully'})


highest_bid = 0
@app.route('/auctions/highest_bid/<string:auction_id>', methods=['PUT'])
def update_highest_bid(auction_id):
    global highest_bid

    print("inside auction highest bid")
    auction = AuctionService.query.filter_by(auction_id = auction_id).first()
    
    # Extract the new bid amount from the request body
    
    print("auction ", auction)

    if auction:
        data = request.get_json()

        if data["highest_bid"]:
            auction.highest_bid = data["highest_bid"]
        
        if  data["customer_id"]:
            auction.customer_id = data["customer_id"]
        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": auction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "auction_id": auction_id
            },
            "message": "auction not found."
        }
    ), 404
    # bid_amount = request.json.get('bid_amount')

    # # Update the highest_bid if the new bid is higher
    # if bid_amount > highest_bid:
    #     highest_bid = bid_amount
    #     response = {'message': 'Highest bid updated successfully'}
    # else:
    #     response = {'message': 'New bid is not higher than current highest bid'}

    # return jsonify(response)


#Get the auction starting price
@app.route("/auctions/starting_price/<string:auction_id>", methods=['GET'])
def get_starting_price(auction_id):
    auction = AuctionService.query.filter_by(auction_id=auction_id).first()

    list = auction.json()
    
    if property:
        return jsonify(
            {
                "code": 200,
                "data": list["starting_price"]
                    
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Auction not found."
        }
    ), 404


# get highest bidder customer id
@app.route("/auctions/<string:auction_id>")
def get_one_auction(auction_id):
    print("over heree")
    auction = AuctionService.query.filter_by(auction_id=auction_id).first()
    list = auction.json()

    if auction:
        return jsonify(
            {
                "code": 200,
                "data": list["customer_id"]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "auction not found."
        }
    ), 404


# check if customer has bid before
@app.route("/auctions/<string:auction_id>/<string:customer_id>")
def check_user_bided(auction_id, customer_id):
    print("over heree")
    auction = AuctionService.query.filter_by(auction_id=auction_id, customer_id=customer_id).first()

    if auction:
        print("true")
        return True
    else:
        print("false")
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
