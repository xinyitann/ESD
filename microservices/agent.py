from app import app, db
from flask import request, jsonify

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)