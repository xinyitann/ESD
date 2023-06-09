# Haven
Haven is an one-stop property bidding platform for users to view property listings, book appointment to view listings and bid for properties.

# Requirements

### Install Google Auth
- pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Project setup
## Access project folder
```
cd ESD
```

## Install dependencies
```
npm install
```

## Run development server
```
npm run serve
```

# Tools used
- [Vue 3](https://vuejs.org/guide/introduction.html)
- [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Docker](https://docs.docker.com/)
- [RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Express.js](https://expressjs.com/)

# Beyond the lab

## Use of multiple programming language for microservices 
Customer.py and agent.py use Javascript and the rest of the microservices use Python

# External services used

## Gmail SMTP Service
Email and Password is stored in environment variables in docker-compose.yml

## Google Calendar API
API Key is stored in an environment variable in docker-compose.yml

## Google Map API
API Key is stored in an environment variable in .env

## PayPal API
Client ID is stored in an environment variable in .env

### Test customer account details
- Email: john_doe_1979@personal.example.com
- Password: R<Zl1dKC

## OneMap API
Access token is stored in an environment variable in .env

### Access token expires every 3 days. To generate an access token:

- Step 1: Sign up for a free account at https://developers.onemap.sg/register/
- Step 2: Check your email inbox for a confirmation email. If it is not in the inbox, check your junk/spam folder.
- Step 3. Copy the confirmation code from the email to complete your registration at https://developers.onemap.sg/confirm_account
- Step 4: After the completion of your registration, an access code will be generated for you
- Step 5: This token will expire in 3 days. You can also retrieve the access token through the authentication service listed at https://developers.onemap.sg/#authentication-service-post


