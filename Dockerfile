FROM python:3.11-alpine

WORKDIR /app

ADD . .

RUN pip install .

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-c gunicorn.config.py", "wsgi:app"]
