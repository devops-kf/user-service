import json
from os import environ

import pika

EXCHANGE_ID = 'user-service-integration-events'


def publish_message(message_type, body):
    connection = pika.BlockingConnection(pika.URLParameters(environ.get('RABBITMQ_URI')))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_ID, exchange_type='fanout')
    properties = pika.BasicProperties(message_type)

    channel.basic_publish(exchange=EXCHANGE_ID, routing_key='', body=json.dumps(body), properties=properties)
