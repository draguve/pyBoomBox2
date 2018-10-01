start CMD /K redis-server
start CMD /K celery worker -A celery_worker.celery --loglevel=info
start CMD /K python pyboombox.py runserver