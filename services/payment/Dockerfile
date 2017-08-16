FROM python:latest
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN python3 -m venv flask
RUN flask/bin/pip3 install -r requirements.txt
CMD flask/bin/python3 payment.py
