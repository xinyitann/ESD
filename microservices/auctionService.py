from app import app,db
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
from os import environ


class AuctionService(db.Model):
    __tablename__ = 'auctions'
        
    auction_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    starting_price = db.Column(db.Float)
    option_fee = db.Column(db.Float)
    highest_bid = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP, nullable=False,server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False,server_default=func.now())


    def __init__(self, start_time, end_time, starting_price,option_fee):
        self.start_time = start_time
        self.end_time = end_time
        self.starting_price = starting_price
        self.option_fee = option_fee
        self.auctions = []
    
    def json(self):
        return {"auction_id": self.auction_id, "start_time": self.start_time ,"end_time": self.end_time, "starting_price": self.starting_price,"option_fee": self.option_fee, "highest_bid": self.highest_bid, "created_at": self.created_at, "updated_at": self.updated_at}



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
        start_time = data['start_time'],
        end_time = data['end_time'],
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

@app.route('/auctions/<string:auction_id>/close', methods=['POST'])
def close_auction(auction_id):
    auction = AuctionService.query.filter_by(auction_id=auction_id).first()
    current_time = datetime.datetime.utcnow()
    if auction is None:
        return jsonify({'error': 'Auction not found'}), 404
    if current_time < auction.start_time:
        return jsonify({'error': 'Auction have not started'}), 400
    if current_time < auction.end_time :
        return jsonify({'message': 'Auction still ongoing'}), 200
    if current_time > auction.end_time:
        return jsonify({'error': 'Auction has ended'}), 400
    auction.end_time = current_time
    db.session.commit()
    return jsonify({'message': 'Auction closed successfully'})


@app.route('/auctions/<string:auction_id>', methods=['PUT'])
def update_highest_bid(auction_id):
     # retrieve the highest bid from the bid microservice
    bid_service_url = "http://127.0.0.1:5500/bids/highest_bid/"  # replace with your bid microservice URL
    response = requests.get(f"{bid_service_url}/bids/highest_bid/{auction_id,customer_id}")
    if response.status_code != 200:
        return jsonify({"code": 404, "message": "Error retrieving highest bid"}), 404

    # extract the highest bid data from the response
    highest_bid_data = response.json()["data"]
    highest_bid = highest_bid_data["highest_bid"]
    customer_id = highest_bid_data["customer_id"]

    # continue with your auction logic using the highest bid data
    ...
    bid_amount = request.json.get('bid_amount')

    if not isinstance(bid_amount, (int, float)):
        return jsonify({'message': 'Invalid bid amount'}), 400

    # Update the highest_bid if the new bid is higher
    if bid_amount > highest_bid:
        highest_bid = bid_amount
        customer_id = highest_bid_data["customer_id"]
        response = {'message': 'Highest bid updated successfully'}
    else:
        response = {'message': 'New bid is not higher than current highest bid'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
