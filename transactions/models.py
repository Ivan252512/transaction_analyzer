from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    id = models.AutoField(primary_key=True)
    receiver = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.transaction_type}: ${self.amount})"
    
    
class FraudulentTransaction(models.Model):
    transaction_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"Fraudulent Transaction ID: {self.transaction_id} - Processed: {self.processed}"

