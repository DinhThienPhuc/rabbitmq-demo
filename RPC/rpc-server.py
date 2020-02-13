#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

queue_name = 'rpc_queue'
channel = connection.channel()
channel.queue_declare(queue=queue_name)

# 0, 1, 2, 3, 4, 5, 6,  7,  8,  9, 10, 11,  12,  13,  14
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377


def getFibonacci(n_th):
    # Get n-th Fibonacci number
    if n_th == 0:
        return 0
    if n_th == 1:
        return 1
    return getFibonacci(n_th-1) + getFibonacci(n_th-2)


def on_request(channel, method, props, body):
    number = int(body)
    print("Fibonacci(%s)" % number)
    response = getFibonacci(number)

    channel.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id),
        body=str(response)
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=queue_name,
    on_message_callback=on_request
)

print("Awaiting RPC requests")
channel.start_consuming()
