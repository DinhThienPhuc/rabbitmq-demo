import pika
import time

source = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(source)
channel = connection.channel()

# Make sure queue and message durable
channel.queue_declare(queue='avengers', durable=True)


def callback(ch, method, properties, body):
    print(' [Avengers] received %r' % body)
    time.sleep(body.count(b'.'))
    print(' [Avengers] done')

    # Forward messages to other consumer when current consumer dies
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
# Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='avengers', on_message_callback=callback)

print(' [Avengers] Waiting for calls. To exit press CTRL+C')
channel.start_consuming()
