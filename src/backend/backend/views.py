import logging
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication  # or remove for []

logger = logging.getLogger('django')

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def ping(request):
    return Response({"message": "Hello from Backend API"})


class EbarimtMerchantTinView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
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
        "url": "http://192.168.1.88:80/shared/test/app-debug.apk"
    }
    return JsonResponse(data)
