import json

from service import user_account_service


class AdminServiceIntegrationEventsConsumer:
    def __init__(self, channel):
        self.exchange_name = 'admin-service-integration-events'
        self.channel = channel

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

        self.queue = channel.queue_declare(queue='')

        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue.method.queue)
        self.channel.basic_consume(queue=self.queue.method.queue, on_message_callback=self.on_message, auto_ack=True)

    def on_message(self, channel, method, properties, message_body):
        message = json.loads(message_body)
        user_account_id = message['user_account_id']

        if properties.content_type == 'AgentRequestApproved':
            user_account_service.handle_agent_request_approved(user_account_id=user_account_id)
        elif properties.content_type == 'AgentRequestRejected':
            user_account_service.handle_agent_request_rejected(user_account_id=user_account_id)
        elif properties.content_type == 'UserAccountMarkedForSuspension':
            user_account_service.handle_user_account_marked_for_suspension(user_account_id=user_account_id)
        else:
            raise RuntimeError('Unhandled message type.')
