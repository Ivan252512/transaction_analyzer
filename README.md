## Topico kafka

docker exec -it kafka_broker kafka-console-consumer --bootstrap-server kafka:9092 --topic transaction_events --from-beginning


## Django docker
docker exec -it django_app bash
python manage.py runserver 0.0.0.0:8000