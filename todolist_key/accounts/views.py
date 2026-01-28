from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  #utenti
    serializer_class = RegisterSerializer  #verifiche
    permission_classes = [permissions.AllowAny]