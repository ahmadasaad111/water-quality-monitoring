import pika
import time
import json

# Wait for RabbitMQ to be ready
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        break
    except:
        print("Waiting for RabbitMQ...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue='waterQualityAlertQueue')

def callback(ch, method, properties, body):
    alert = json.loads(body)
    print("🚨 ALERT RECEIVED:", alert)

channel.basic_consume(queue='waterQualityAlertQueue', on_message_callback=callback, auto_ack=True)
print("Alert reporter is running...")
channel.start_consuming()
