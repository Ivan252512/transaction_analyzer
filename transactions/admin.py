from django.contrib import admin
from .models import Transaction, FraudulentTransaction

admin.site.register(Transaction)
admin.site.register(FraudulentTransaction)