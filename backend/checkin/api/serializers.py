from rest_framework import serializers

class CheckInQRSerializer(serializers.Serializer):
    qr_payload = serializers.CharField()