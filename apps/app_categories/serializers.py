from rest_framework import serializers


from .models import Category





class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    
    
    class Meta:
        model = Category
        fields = ["id", "name", "category_type", "created_at"]
        read_only_fields = ["id"]
        
