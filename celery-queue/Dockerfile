FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV SPOTIFY_USERNAME draguve
ENV SPOTIFY_CLIENT_ID 1f436bc4fe2b4926b1cb4e368065db96
ENV SPOTIFY_CLIENT_SECRET 1b6aa3fccad34700a8c6ae76d09c29a7
ENV SPOTIFY_REDIRECT_URL http://draguve.hopto.org

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info