FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./makebooking.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./makebooking.py"]
# works but have output as Fail to add booking (agent microservice) 
# tested using: 
# {
#     "agent_id":1,
#     "customer_id":1,
#     "property_id":1,
#     "datetimestart":"2023-04-21 13:00:00",
#     "datetimeend":"2023-04-21 15:00:00",
#     "status":"pending"
# }