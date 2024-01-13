# Running background tasks

The `background_tasks` app controls background execution. If it is in `INSTALLED_APPS`, stuff can be run in background. If it is not, stuff will block the request handler.

As a general rule, everything that is supposed to be run in a background task should check for `'background_tasks' in settings.INSTALLED_APPS` and run synchronously if it's not (unless it would be insane). See an example

Production deployments are expected to use `background_tasks`.

To use `background_tasks`, you need an AMQP 0.91 broker such as RabbitMQ. Not tested with anything else, such as ActiveMQ.

## Getting started

To install and configure RabbitMQ and the associated Python modules, do

    sudo apt-get install rabbitmq-server
    sudo -Hu rabbitmq rabbitmqctl add_vhost kompassidev
    sudo -Hu rabbitmq rabbitmqctl add_user kompassidev kompassidev
    sudo -Hu rabbitmq rabbitmqctl set_permissions -p kompassidev kompassidev '.*' '.*' '.*'

    export BROKER_URL=rabbitmq://kompassidev:kompassidev@localhost/kompassidev

By convention we use `KOMPASSI_INSTALLATION_SLUG` as the vhost name and user name in RabbitMQ. In development, we also use it as the password. In production, you should set up a secure password.

Now you should be able to

    celery -A kompassi worker

Note that the Celery app name `kompassi` is hardcoded into `kompassi/celery_app.py` and is not the `KOMPASSI_INSTALLATION_SLUG` from `settings.py`. Please dedicate a RabbitMQ vhost for each Kompassi instance.
