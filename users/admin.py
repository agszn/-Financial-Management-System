from django.contrib import admin
from .models import *

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'date', 'flagged', 'risk_score')

@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'created_at')


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit_card_number', 'reason')