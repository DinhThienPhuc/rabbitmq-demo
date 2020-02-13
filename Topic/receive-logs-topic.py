#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

exchange_name = 'topic-logs'
exchange_type = 'topic'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=binding_key
    )

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True)

channel.start_consuming()
