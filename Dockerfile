FROM python:3.11

WORKDIR /app

# Dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Code
COPY bot.py bot.py

