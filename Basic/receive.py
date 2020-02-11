#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='avengers')


def callback(ch, method, properties, body):
    print(' [Avengers] received %r' % body)


channel.basic_consume(queue='avengers', auto_ack=True,
                      on_message_callback=callback)

print(' [Avengers] Waiting for calls. To exit press CTRL+C')
channel.start_consuming()
