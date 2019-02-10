FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV SPOTIFY_USERNAME username
ENV SPOTIFY_CLIENT_ID client_id
ENV SPOTIFY_CLIENT_SECRET client_secret
ENV SPOTIFY_REDIRECT_URL redirect_url

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info