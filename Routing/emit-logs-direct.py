#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

exchange_name = 'direct-logs'
exchange_type = 'direct'
default_message = 'info: Hello World!'
message = sys.argv[1] or default_message
severity = sys.argv[2] if len(sys.argv) > 2 else 'info'

channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

channel.basic_publish(
    exchange=exchange_name,
    routing_key=severity,
    body=message
)

print(' [x] Sent %r' % message)
connection.close()
