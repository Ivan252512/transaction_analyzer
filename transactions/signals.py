from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from .kafka_producer import send_transaction_event

@receiver(post_save, sender=Transaction)
def transaction_saved(sender, instance, created, **kwargs):
    if created:
        transaction_data = {
            "id": instance.id,
            "sender": instance.sender,
            "receiver": instance.receiver,
            "amount": float(instance.amount),
            "transaction_type": instance.transaction_type,
            "created_at": instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        send_transaction_event(transaction_data)
