FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app app
COPY assets assets
COPY bot bot
COPY config.py config.py
COPY main.py main.py

CMD ["python3", "main.py"]
