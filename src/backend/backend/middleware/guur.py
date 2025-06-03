import requests
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from backend.middleware.serializers import *
from backend.middleware.utils import *


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def guurAuthToken(request):
    serializer = GuurAuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print("serializer.is_valid() : ", serializer.is_valid())
    data = serializer.validated_data
    print("serializer.validated_data : ", serializer.validated_data)
    url = settings.GUUR_URL + "/api/auth/get_tokens"
    params = {'username': data.get('username'), 'password': data.get('password')}
    response = requests.get(url, params=params)
    return Response(response.json())


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def guurGetProduct(request):
    serializer = GuurProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print("serializer.is_valid() : ", serializer.is_valid())
    data = serializer.validated_data
    getToken()
    print("serializer.validated_data : ", serializer.validated_data)
    url = settings.GUUR_URL + "/api/product.product"
    params = {'username': data.get('username'), 'password': data.get('password')}
    response = requests.get(url, params=params)
    return Response(response.json())