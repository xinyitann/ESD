const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Define your routes and database connections here
app.use(bodyParser.json()); // to parse JSON bodies
app.listen(5003, function() {
    console.log('Server listening on port 5003');
});

var mysql = require('mysql2');

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "property_management"
});

class Agent {
    constructor(agent_id, name, phone, email) {
        this.agent_id = agent_id;
        this.name = name;
        this.phone = phone;
        this.email = email;
    }

    json() {
        return {
            "agent_id": this.agent_id,
            "name": this.name,
            "phone": this.phone,
            "email": this.email
        }
    }
}


//GET AGENT
app.get('/agent/:agent_id', function(req, res) {
    const agent_id = req.params.agent_id;
    con.query("SELECT * FROM agent WHERE agent_id = ?", [agent_id], function (err, result) {
        if (err) throw err;

        if (result.length > 0) {
            const agent = new Agent(result[0].agent_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": agent.json()
            });
        } else {
            res.status(404).json({
                "code": 404,
                "message": "agent not found."
            });
        }
    });
});

//ADD AN AGENT
app.post('/agent', function(req, res) {
    console.log(req.body); // log the request body
    const { agent_id, name, phone, email } = req.body;
    const agent = new Agent(agent_id, name, phone, email);

    con.query("INSERT INTO agent SET ?", agent, function (err, result) {
        if (err) {
            console.error(err);
            res.status(500).json({ code: 500, message: "An error occurred creating the agent." });
            return;
        }
        console.log(result);
        res.status(201).json({ code: 201, data: agent.json() });
    });
});

// UPDATE AN AGENT
app.put('/agent/:agent_id', function(req, res) {
    const agent_id = req.params.agent_id;
    const { name, phone, email } = req.body;
    con.query("UPDATE agent SET name = ?, phone = ?, email = ? WHERE agent_id = ?", [name, phone, email, agent_id], function (err, result) {
        if (err) {
            console.error(err);
            console.error(err.message);
            res.status(404).json({
                "code": 404,
                "data": {
                    "agent_id": agent_id
                },
                "message": "agent not found."
            });
            return;
        }
        if (result.affectedRows === 0) {
            res.status(404).json({
                "code": 404,
                "data": {
                    "agent_id": agent_id
                },
                "message": "agent not found."
            });
            return;
        }
        con.query("SELECT * FROM agent WHERE agent_id = ?", [agent_id], function (err, result) {
            if (err) throw err;

            const agent = new Agent(result[0].agent_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": agent.json()
            });
        });
    });
});

// DELETE AN AGENT
app.delete('/agent/:agent_id', function(req, res) {
    const agent_id = req.params.agent_id;
    con.query("DELETE FROM agent WHERE agent_id = ?", [agent_id], function (err, result) {
        if (err) {
            console.error(err);
            res.status(500).json({ code: 500, message: "An error occurred deleting the agent." });
            return;
        }
        if (result.affectedRows === 0) {
            res.status(404).json({
                "code": 404,
                "data": {
                    "agent_id": agent_id
                },
                "message": "agent not found."
            });
            return;
        }
        res.json({
            "code": 200,
            "data": {
                "agent_id": agent_id
            }
        });
    });
});


//GET AGENT'S ID FROM EMAIL
app.get('/agent/get_id_by_email/:email', function(req, res) {
    const email = req.params.email;
    con.query("SELECT * FROM agent WHERE email = ?", [email], function (err, result) {
        if (err) throw err;

        if (result.length > 0) {
            const agent = new Agent(result[0].agent_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": agent.json()
            });
        } else {
            res.status(404).json({
                "code": 404,
                "message": "agent not found."
            });
        }
    });
});