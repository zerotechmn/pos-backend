import requests
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from backend.middleware.serializers import *
from backend.middleware.utils import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication  # or remove for []


class GuurAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GuurAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("serializer.is_valid() : ", serializer.is_valid())
        data = serializer.validated_data
        print("serializer.validated_data : ", serializer.validated_data)
        UserCreate(data)
        url = settings.GUUR_URL + "/api/auth/get_tokens"
        params = {'username': data.get('username'), 'password': data.get('password')}
        response = requests.get(url, params=params)
        return Response(response.json())


class GuurGetProductLineView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def termial_attribute(self):
        version = self.request.META.get('HTTP_VERSION')
        print("version : ", version)
    
    def post(self, request):
        serializer = GuurBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        token = getToken()
        headers = {
            "Access-token": token.get("access_token")
        }
        params = {
            "filters": f'[["shts_code", "=", "{data.get("shts_code")}"]]'
        }
        url = settings.GUUR_URL + "/api/shts.register.line"
        response = requests.get(url, headers=headers, params=params)
        return Response(response.json())


class GuurGetWareHouseView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GuurBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        token = getToken()
        headers = {
            "Access-token": token.get("access_token")
        }
        params = {
            "filters": f'[["shts_code", "=", "{data.get("shts_code")}"]]'
        }
        url = settings.GUUR_URL + "/api/shts.register"
        response = requests.get(url, headers=headers, params=params)
        return Response(response.json())


class GuurGetPumpView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuurBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        token = getToken()
        headers = {
            "Access-token": token.get("access_token")
        }
        params = {
            "filters": f'[["shts_code", "=", "{data.get("shts_code")}"]]'
        }
        url = settings.GUUR_URL + "/api/pump.mapping"
        response = requests.get(url, headers=headers, params=params)
        return Response(response.json())


class GuurGetProductView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuurProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = getToken()
        headers = {
            "Access-token": token.get("access_token")
        }
        params = {
            "query": f'[["shts_code", "=", "{data.get("shts_code")}"]]'
        }
        url = settings.GUUR_URL + "/api/product.product"
        response = requests.get(url, headers=headers, params=params)

        return Response(response.json())