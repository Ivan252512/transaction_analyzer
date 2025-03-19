import json
import logging
import numpy as np
import pandas as pd
from datetime import timedelta
from kafka import KafkaConsumer
from django.conf import settings
from django.db.models import Sum, Q
from .models import Transaction, FraudulentTransaction
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# Cargar el modelo de TensorFlow
model = keras.models.load_model("fraud_detection_model.h5")

# Configurar el StandardScaler con los valores de media y desviación estándar correctos
scaler = StandardScaler()
scaler.mean_ = np.array([5050, 0.5, 0.5, 5, 4500])  # Estos valores deberían ser ajustados basados en el entrenamiento real del modelo
scaler.scale_ = np.array([2900, 0.5, 0.5, 3, 3200])

def check_history(transaction):
    """Función para verificar el historial de transacciones del sender y receiver."""
    sender_exists = Transaction.objects.filter(sender=transaction['sender']).exists()
    receiver_exists = Transaction.objects.filter(receiver=transaction['receiver']).exists()

    # Calcular el rango de tiempo de un minuto antes de la transacción actual
    one_minute_ago = transaction['created_at'] - timedelta(minutes=1)
    transactions_in_last_minute = Transaction.objects.filter(
        Q(sender=transaction['sender']) | Q(receiver=transaction['receiver']),
        created_at__gte=one_minute_ago
    )
    count_transactions = transactions_in_last_minute.count()
    sum_amounts = transactions_in_last_minute.aggregate(Sum('amount'))['amount__sum'] or 0

    return sender_exists, receiver_exists, count_transactions, sum_amounts

def is_fraudulent(transaction_data):
    """Función para determinar si una transacción es fraudulenta."""
    try:
        sender_exists, receiver_exists, count_transactions, sum_amounts = check_history(transaction_data)
        
        # Preparar las características para el modelo
        features = np.array([[
            1 if transaction_data["amount"] > 5000 else 0,
            1 if sender_exists else 0,
            1 if receiver_exists else 0,
            1 if count_transactions > 2 else 0,
            1 if sum_amounts > 6000 else 0
        ]])
        
        # Predecir fraude directamente con características binarias
        prediction = model.predict(features)
        is_fraud = prediction[0][0] > 0.5

        logging.info(f"Predicción: {is_fraud} | Monto: {transaction_data['amount']} | Score: {prediction[0][0]:.4f} | Transacciones previas: {count_transactions} | Suma previa: {sum_amounts}")
        return is_fraud
    except Exception as e:
        logging.error(f"Error en predicción: {e}")
        return False


def start_kafka_consumer():
    """Función para iniciar el consumidor de Kafka."""
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
        transaction_data['created_at'] = pd.to_datetime(transaction_data['created_at'], utc=True)  # Asegurarse de que la fecha está en UTC
        logging.info(f"Recibido: {transaction_data}")

        if is_fraudulent(transaction_data):
            transaction_id = transaction_data["id"]
            if not FraudulentTransaction.objects.filter(transaction_id=transaction_id).exists():
                FraudulentTransaction.objects.create(transaction_id=transaction_id, processed=False)
                logging.info(f"FRAUDE DETECTADO Y GUARDADO: {transaction_data}")

