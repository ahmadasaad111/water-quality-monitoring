import pika
import json
import time

critical_readings = []

# Wait for RabbitMQ to be ready
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        break
    except:
        print("Waiting for RabbitMQ...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue='waterQualityQueue')
channel.queue_declare(queue='waterQualityAlertQueue')

def callback(ch, method, properties, body):
    global critical_readings
    data = json.loads(body)
    ph = data.get("value")

    if ph < 5.0 or ph > 9.0:
        critical_readings.append(ph)
        print(f"Critical pH reading: {ph}")

        if len(critical_readings) >= 3:
            alert = json.dumps({
                "alert": "CRITICAL_WATER_QUALITY",
                "values": critical_readings[-3:]
            })
            channel.basic_publish(exchange='', routing_key='waterQualityAlertQueue', body=alert)
            print("Alert published.")
    else:
        critical_readings = []

channel.basic_consume(queue='waterQualityQueue', on_message_callback=callback, auto_ack=True)
print("Processor is running...")
channel.start_consuming()
