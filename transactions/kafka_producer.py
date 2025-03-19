from kafka import KafkaProducer
import json
from django.conf import settings

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def send_transaction_event(transaction_data):
    producer = get_kafka_producer()
    producer.send(settings.KAFKA_TOPIC, transaction_data)
    producer.flush()
