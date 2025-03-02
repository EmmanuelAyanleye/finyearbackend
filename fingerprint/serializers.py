from rest_framework import serializers

class FingerprintSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    fingerprint = serializers.CharField()  # This will hold the Base64 fingerprint string
