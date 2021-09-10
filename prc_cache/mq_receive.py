from django.test import TestCase
import time
# Create your tests here.

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='aa')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.')*10)
    print("[x] done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='hello',
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
