from rest_framework import serializers

class YooKassaCreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()