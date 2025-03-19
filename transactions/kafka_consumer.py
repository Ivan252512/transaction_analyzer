import json
import logging
import numpy as np
from kafka import KafkaConsumer
from django.conf import settings
from .models import FraudulentTransaction
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)

model = keras.models.load_model("fraud_detection_model.h5")

scaler = StandardScaler()
scaler.mean_ = np.array([5050])
scaler.scale_ = np.array([2900])

def is_fraudulent(transaction_data):
    try:
        monto_scaled = scaler.transform(np.array([[transaction_data["amount"]]]))
        prediccion = model.predict(monto_scaled)
        fraude = prediccion[0][0] > 0.5
        logging.info(f"Predicción: {fraude} | Monto: {transaction_data['amount']} | Score: {prediccion[0][0]:.4f}")
        return fraude
    except Exception as e:
        logging.error(f"Error en predicción: {e}")
        return False

def start_kafka_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )

    logging.info("Kafka Consumer escuchando...")

    for message in consumer:
        transaction_data = message.value
        logging.info(f"Recibido: {transaction_data}")

        if is_fraudulent(transaction_data):
            transaction_id = transaction_data["id"]
            if not FraudulentTransaction.objects.filter(transaction_id=transaction_id).exists():
                FraudulentTransaction.objects.create(transaction_id=transaction_id, processed=False)
                logging.info(f"FRAUDE DETECTADO Y GUARDADO: {transaction_data}")
