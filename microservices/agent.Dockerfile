# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt amqp.reqs.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
# COPY ./agent.py ./app.py ./
# CMD [ "python", "./agent.py" ]

FROM node:latest

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY agent.js ./

EXPOSE 5003

CMD [ "node", "agent.js" ]
