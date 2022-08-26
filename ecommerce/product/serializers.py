from dataclasses import field
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields='__all__'
        # fields = ('id', 'username', 'email', 'password', 'token',)
        # extra_kwargs = {'password': {'write_only': True}}

    