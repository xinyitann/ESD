# need changes for post!
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app import app, db
class Agent(db.Model):
    __tablename__ = 'agent'

    agent_id = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(20), nullable=False)

    def __init__(self, agent_id, name, phone, email):
        self.agent_id = agent_id
        self.name = name
        self.phone = phone
        self.email = email

    def json(self):
        return {"agent_id": self.agent_id, "name": self.name, "phone": self.phone, "email": self.email}

# GET ONE AGENT
@app.route("/agent/<agent_id>")
def find_agent(agent_id):
    agent_id = int(agent_id)
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if agent:
        return jsonify(
            {
                "code": 200,
                "data": agent.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "agent not found."
        }
    ), 404

# ADDING A AGENT
@app.route("/agent", methods=['POST'])
def create_agent():
    data = request.get_json()
    agent = Agent(**data)

    try:
        db.session.add(agent)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the agent."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": agent.json()
        }
    ), 201

# UPDATE AGENT DETAILS
@app.route("/agent/<string:agent_id>", methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if agent:
        data = request.get_json()
        if data['name']:
            agent.name = data['name']
        if data['phone']:
            agent.phone = data['phone']
        if data['email']:
            agent.email = data['email'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": agent.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "agent_id": agent_id
            },
            "message": "agent not found."
        }
    ), 404

#DELETE AGENT
@app.route("/agent/<string:agent_id>", methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if agent:
        db.session.delete(agent)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "agent_id": agent_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "agent_id": agent_id
            },
            "message": "agent not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
