FROM python:2.7
add . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python ragbshortener/ragbshortener.py --redis-host redis_server

