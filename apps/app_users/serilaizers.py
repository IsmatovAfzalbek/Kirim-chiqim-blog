import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


from .models import CustomUser




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']


    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError({"error": "Bu email band."})
        return email


    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if not re.match(pattern, password):
            raise ValidationError({
                "error": "Parol kamida 8 ta belgidan iborat bo'lishi, kamida 1 ta katta harf, kichik harf, raqam va maxsus belgi (@$!%*?&) bo'lishi kerak."
            })

        if password != confirm_password:
            raise ValidationError({"error": "Parollar bir-biriga mos emas."})

        return attrs
    
    
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)
        
        return user
    
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
    
        user = authenticate(email=email, password=password)
        
        if not user:
            raise ValidationError({
                "message": "Login yoki Parol xato",
            })

        attrs["user"] = user
        return attrs
    


class ProfileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']
        
        
        
class ProfileUpdateSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']   
