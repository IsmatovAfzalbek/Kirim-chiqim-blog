from rest_framework import serializers

from .models import Currency, ExchangeRate




class CurrencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]
        read_only_fields = ["id"]
        
    
class ExchangeRateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    
    class Meta:
        model = ExchangeRate
        fields = ["id", "currency", "rate_uzs", "date", "created_at"]
        read_only_fields = ["id"]
    
    
    
    