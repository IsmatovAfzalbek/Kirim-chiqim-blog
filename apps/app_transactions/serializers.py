from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.app_currencies.models import ExchangeRate
from .models import Transaction, RecurringTransaction





class TransactionSerializer(serializers.ModelSerializer):
    amount_uzs = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "account", "category", "transaction_type",
            "amount", "currency", "amount_uzs", "description",
            "date", "created_at"
        ]
        read_only_fields = ["id", "amount_uzs"]


    def create(self, validated_data):
        date = validated_data.get("date")
        currency = validated_data.get("currency")

        try:
            exchange_rate = ExchangeRate.objects.get(currency=currency, date=date)
            amount_uzs = validated_data["amount"] * exchange_rate.rate_uzs
        except ExchangeRate.DoesNotExist:
            raise ValidationError({
                "error": f"{currency.code} valyutasi uchun {date} sanasida kurs topilmadi."
            })

        validated_data["amount_uzs"] = amount_uzs
        return super().create(validated_data)



class RecurringTransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = RecurringTransaction
        fields = [
            "id", "account", "category", "transaction_type",
            "title", "amount", "currency", "frequency",
            "start_date", "end_date", "next_run_date", "is_active", "created_at"
        ]
        read_only_fields = ["id"]
    
    
    