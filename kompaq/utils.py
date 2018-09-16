# encoding: utf-8

'''
Public API for the outbound AMQP notifications. It is safe to import this module without the
'kompaq' application being in INSTALLED_APPS.
'''

import json

from django.conf import settings

from pika.connection import URLParameters
from pika import BlockingConnection


_channel = None
_exchanges_we_declared = set()

KOMPAQ_VERSION = '0.1'


def _get_channel():
    global _channel
    assert 'kompaq' in settings.INSTALLED_APPS

    if not _channel:
        connection = BlockingConnection(URLParameters(settings.KOMPAQ_URL))
        _channel = connection.channel()

    return _channel


def _get_exchange_for_model_instance(instance, exchange_type='fanout'):
    assert 'kompaq' in settings.INSTALLED_APPS

    model = instance.__class__
    meta = model._meta
    exchange_name = '{prefix}.{app_label}.{model_name}'.format(
        prefix='kompassi', # TODO NEW_INSTALLATION_SLUG
        app_label=meta.app_label,
        model_name=meta.model_name,
    )

    if exchange_name not in _exchanges_we_declared:
        channel = _get_channel()
        channel.exchange_declare(
            exchange=exchange_name,
            type=exchange_type,
            durable=True,
        )

    return exchange_name


def _format_message(instance, action):
    model = instance.__class__
    meta = model._meta

    return dict(instance.as_dict(),
        _type=meta.label,
        _action=action,
        _version=KOMPAQ_VERSION,
    )


def send_update(instance, action='created'):
    if 'kompaq' not in settings.INSTALLED_APPS:
        return

    channel = _get_channel()
    exchange = _get_exchange_for_model_instance(instance)
    body = json.dumps(_format_message(instance, action))

    # routing_key='' – fanout exchange
    channel.basic_publish(exchange=exchange, routing_key='', body=body)
