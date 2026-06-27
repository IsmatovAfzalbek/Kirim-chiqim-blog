from rest_framework import serializers


from.models import Account




class AccountSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    
    
    class Meta:
        model = Account
        fields = ["id", "name", "account_type", "balance", "currency", "created_at"]
        read_only_fields = ["id"]
