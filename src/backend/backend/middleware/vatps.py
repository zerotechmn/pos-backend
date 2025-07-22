import json
import requests
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication  # or remove for []
from backend.middleware.serializers import *
from backend.middleware.utils import *


class EBarimtReceiptransactionView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = eBarimtReceiptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        regno = data.get("regno")
        tin = getMerchantTin(regno)
        
        url = settings.EBARIMT_30_URL + "/api/v1/pos/receipt"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + settings.EBARIMT_TOKEN
        }
        if tin:
            data['merchantTin'] = tin
        print("valid data ", data)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("response ", response.json())

        return Response(response.json())
