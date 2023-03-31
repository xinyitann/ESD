FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./property.py ./app.py ./customer.py ./auctionService.py ./agent.py ./
CMD [ "python", "./property.py" ]
