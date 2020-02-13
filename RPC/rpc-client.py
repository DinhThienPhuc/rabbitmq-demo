#!/user/bin/env python
import pika
import uuid
import sys


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.calback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.calback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.queue = 'rpc-queue'

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.calback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
number = int(sys.argv[1]) if len(sys.argv) >= 2 else 10

print('Requesting Fibonacci({})'.format(number))
response = fibonacci_rpc.call(number)
print('Got %r' % response)
