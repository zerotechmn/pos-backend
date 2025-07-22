import json
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from backend.remote.remote_utils import *

class RemotePTSView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def termial_attribute(self):
        version = self.request.META.get('HTTP_VERSION')
        print("version : ", version)

    def post(self, request):
        serializer = GuurBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        token = create_websocket()
        headers = {
            "Access-token": token.get("access_token")
        }
        params = {
            "filters": f'[["shts_code", "=", "{data.get("shts_code")}"]]'
        }
        url = settings.GUUR_URL + "/api/shts.register.line"
        response = requests.get(url, headers=headers, params=params)
        return Response(response.json())
