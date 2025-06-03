from rest_framework import serializers

class GuurAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

class GuurProductSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100, required=True)