FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./bids.py ./customer.py ./auctionService.py ./app.py ./
CMD [ "python", "./bids.py"]