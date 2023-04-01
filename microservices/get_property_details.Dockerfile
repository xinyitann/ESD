FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./property.py ./invokes.py ./amqp_setup.py ./auctionService.py ./agent.py ./
CMD [ "python", "./get_property_details.py" ]