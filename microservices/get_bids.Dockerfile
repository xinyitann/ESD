FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./get_bids.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./get_bids.py" ]
# works but have issues with property microservice
# tested using: http://localhost:5029/getbids/1
# got: {
#     "code": 500,
#     "message": "get_bids.py internal error: 'data' at <class 'KeyError'>: get_bids.py: line 25"
# }