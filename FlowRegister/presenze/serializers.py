from rest_framework import serializers
from .models import Presenza

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenza
        fields = ['id', 'participante', 'giorno', 'stato']