#!/usr/bin/env python
from datetime import datetime
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='avengers')
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
channel.basic_publish(exchange='', routing_key='avengers', body=dt_string)
print(' [Cap] sent \'Assemble!\'')

connection.close()
