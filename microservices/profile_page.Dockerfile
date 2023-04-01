FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./profile_page.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./profile_page.py" ]