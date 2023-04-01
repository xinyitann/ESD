FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./app.py ./
COPY ./auctionService.py ./
COPY ./customer.py ./
COPY ./property.py ./
COPY ./bids.py ./
CMD [ "python", "./make_bid.py"]