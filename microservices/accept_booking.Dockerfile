FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./booking.py .
COPY ./customer.py .
COPY ./accept_booking.py .
CMD [ "python", "./booking.py" ]