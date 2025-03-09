from rest_framework import serializers
from .models import FingerprintData

class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = FingerprintData
        fields = ['student', 'template']

