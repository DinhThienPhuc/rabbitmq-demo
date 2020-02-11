import sys
import pika

source = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(source)
channel = connection.channel()

# Make sure queue and message durable
channel.queue_declare(queue='avengers', durable=True)

message = ''.join(sys.argv[1:]) or 'Hello World!'
channel.basic_publish(exchange='',
                      routing_key='avengers',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))  # Make sure queue and message durable

print(" [Captain America] sent %r" % message)
