from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from . import serializers
from usermanagement.permissions import CurrentUserOrAdminOrReadOnly
from rest_framework import viewsets
from .models import Product
from rest_framework import permissions



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-updated_date')
    serializer_class = serializers.ProductSerializer
    #permission_classes = [permissions.IsAuthenticated]


