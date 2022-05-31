from os import environ

import pika

from integration.consumer import AdminServiceIntegrationEventsConsumer

connection = pika.BlockingConnection(pika.URLParameters(environ.get('RABBITMQ_URI')))
channel = connection.channel()

admin_service_consumer = AdminServiceIntegrationEventsConsumer(channel)

channel.start_consuming()
channel.close()
