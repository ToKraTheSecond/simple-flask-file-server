FROM python:3.11-slim

ENV FLASK_APP=file_server.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run"]