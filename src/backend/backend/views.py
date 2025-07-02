import logging
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse

logger = logging.getLogger('django')

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def ping(request):
    return Response({"message": "Hello from Backend API"})


@api_view(['GET'])
@authentication_classes([])
def ebarimtMerchantTin(request):
    logger.info(f"RequestData : {request.query_params}")
    regno = request.query_params.get("regno")
    if regno in [None, ""]:
        return Response("")
    
    url = "https://api.ebarimt.mn/api/info/check/getTinInfo"
    headers = {"Accept": "application/json"}
    data = {
        "regNo": regno
    }
    response = requests.get(url, headers=headers, data=data)
    logger.info(f"Response : {response.json()}")

    return Response(response.json())


def update_info(request):
    data = {
        "version": "1.0.1",
        "description": "Update available",
        "url": "http://192.168.1.145:80/shared/test/app-debug.apk"
    }
    return JsonResponse(data)
