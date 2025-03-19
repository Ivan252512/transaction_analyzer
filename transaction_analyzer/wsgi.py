"""
WSGI config for transaction_analyzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import threading
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transaction_analyzer.settings')

application = get_wsgi_application()

from transactions.kafka_consumer import start_kafka_consumer

def run_kafka_consumer():
    start_kafka_consumer()

consumer_thread = threading.Thread(target=run_kafka_consumer, daemon=True)
consumer_thread.start()
