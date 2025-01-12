FROM python4.14.0a3-alpine

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]