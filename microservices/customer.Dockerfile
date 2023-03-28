FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./customer.py .
COPY ./app.py .
CMD [ "python", "./customer.py" ]

# Dockerfile for customer.js
# FROM node:14
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# EXPOSE 5700
# CMD [ "node", "customer.js" ]