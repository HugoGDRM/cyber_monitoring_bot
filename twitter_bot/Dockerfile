FROM python:3.11

WORKDIR /app

ENTRYPOINT [ "python3", "bot.py" , "twitter.py", "text_razor.py"]

# Dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Code
#COPY *.py *.ini ./
