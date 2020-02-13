#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

exchange_name = 'topic-logs'
exchange_type = 'topic'
default_message = 'info: Hello World!'
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = sys.argv[2] or default_message

channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=message
)

print(' [x] Sent %r' % message)
connection.close()
