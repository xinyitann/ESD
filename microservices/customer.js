const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Define your routes and database connections here
app.use(bodyParser.json()); // to parse JSON bodies
app.listen(5700, function() {
    console.log('Server listening on port 5700');
});

var mysql = require('mysql2');
const con = mysql.createConnection(process.env.dbURL);

// var con = mysql.createConnection({
//     host: "host.docker.internal",
//     user: "is213",
//     password: "",
//     database: "property_management"
// });

class Customer {
    constructor(customer_id, name, phone, email) {
        this.customer_id = customer_id;
        this.name = name;
        this.phone = phone;
        this.email = email;
    }

    json() {
        return {
            "customer_id": this.customer_id,
            "name": this.name,
            "phone": this.phone,
            "email": this.email
        }
    }
}


//GET CUSTOMER
app.get('/customer/:customer_id', function(req, res) {
    const customer_id = req.params.customer_id;
    con.query("SELECT * FROM customer WHERE customer_id = ?", [customer_id], function (err, result) {
        if (err) throw err;

        if (result.length > 0) {
            const customer = new Customer(result[0].customer_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": customer.json()
            });
        } else {
            res.status(404).json({
                "code": 404,
                "message": "customer not found."
            });
        }
    });
});

//ADD AN CUSTOMER
app.post('/customer', function(req, res) {
    console.log(req.body); // log the request body
    const { customer_id, name, phone, email } = req.body;
    const customer = new Customer(customer_id, name, phone, email);

    con.query("INSERT INTO customer SET ?", customer, function (err, result) {
        if (err) {
            console.error(err);
            res.status(500).json({ code: 500, message: "An error occurred creating the customer." });
            return;
        }
        console.log(result);
        res.status(201).json({ code: 201, data: customer.json() });
    });
});

// UPDATE AN CUSTOMER
app.put('/customer/:customer_id', function(req, res) {
    const customer_id = req.params.customer_id;
    const { name, phone, email } = req.body;
    con.query("UPDATE customer SET name = ?, phone = ?, email = ? WHERE customer_id = ?", [name, phone, email, customer_id], function (err, result) {
        if (err) {
            console.error(err);
            console.error(err.message);
            res.status(404).json({
                "code": 404,
                "data": {
                    "customer_id": customer_id
                },
                "message": "customer not found."
            });
            return;
        }
        if (result.affectedRows === 0) {
            res.status(404).json({
                "code": 404,
                "data": {
                    "customer_id": customer_id
                },
                "message": "customer not found."
            });
            return;
        }
        con.query("SELECT * FROM customer WHERE customer_id = ?", [customer_id], function (err, result) {
            if (err) throw err;

            const customer = new Customer(result[0].customer_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": customer.json()
            });
        });
    });
});

// DELETE AN CUSTOMER
app.delete('/customer/:customer_id', function(req, res) {
    const customer_id = req.params.customer_id;
    con.query("DELETE FROM customer WHERE customer_id = ?", [customer_id], function (err, result) {
        if (err) {
            console.error(err);
            res.status(500).json({ code: 500, message: "An error occurred deleting the customer." });
            return;
        }
        if (result.affectedRows === 0) {
            res.status(404).json({
                "code": 404,
                "data": {
                    "customer_id": customer_id
                },
                "message": "customer not found."
            });
            return;
        }
        res.json({
            "code": 200,
            "data": {
                "customer_id": customer_id
            }
        });
    });
});


//GET CUSTOMER'S ID FROM EMAIL
app.get('/customer/get_id_by_email/:email', function(req, res) {
    const email = req.params.email;
    con.query("SELECT * FROM customer WHERE email = ?", [email], function (err, result) {
        if (err) throw err;

        if (result.length > 0) {
            const customer = new Customer(result[0].customer_id, result[0].name, result[0].phone, result[0].email);
            res.json({
                "code": 200,
                "data": customer.json()
            });
        } else {
            res.status(404).json({
                "code": 404,
                "message": "customer not found."
            });
        }
    });
});


