from __future__ import absolute_import

from turska.celery_app import app


@app.task
def ping():
    return "pong"
