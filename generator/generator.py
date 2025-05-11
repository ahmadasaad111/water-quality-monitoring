import pika
import time
import random
import json

# Wait for RabbitMQ to be ready
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        break
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ to be ready...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue='waterQualityQueue')

def generate_ph():
    return round(random.uniform(3.0, 10.0), 2)

while True:
    ph = generate_ph()
    message = json.dumps({'parameter': 'pH', 'value': ph})
    channel.basic_publish(exchange='', routing_key='waterQualityQueue', body=message)
    print(f"Sent reading: pH = {ph}")
    time.sleep(5)
