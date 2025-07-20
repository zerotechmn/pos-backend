import requests
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from backend.middleware.serializers import *
from backend.middleware.utils import *


def eBarimtReceiptransaction(request):
    serializer = eBarimtReceiptSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    print("valid data ", data)
    regno = data.get("regno")
    tin = getMerchantTin(regno)
    
    url = "https://api.ebarimt.mn/api/info/check/getTinInfo"
    headers = {"Accept": "application/json"}
    # data.get("merchantTin") = tin
    print("data ", data)
    response = requests.get(url, headers=headers, data=data)

    return Response(response.json())
