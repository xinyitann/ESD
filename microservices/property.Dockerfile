FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./property.py ./
COPY ./app.py ./
COPY ./customer.py ./
COPY ./auctionService.py ./
COPY ./agent.py ./

CMD [ "python", "./property.py" ]
