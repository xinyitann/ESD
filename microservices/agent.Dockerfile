FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./agent.py .
COPY ./app.py .
CMD [ "python", "./agent.py" ]

# Dockerfile for agent.js
# FROM node:14
# WORKDIR /app
# COPY package*.json ./
# RUN npm install
# COPY . .
# EXPOSE 5003
# CMD [ "node", "customer.js" ]