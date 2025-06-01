import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ping(request):
    return Response({"message": "Hello from Backend API"})

@api_view(['GET'])
def ebarimtMerchantTin(request):
    regno = request.data.get("regno")
    if regno in [None, ""]: 
        return Response("")
    
    url = "https://api.ebarimt.mn/api/info/check/getTinInfo"
    headers = {"Accept": "application/json"}
    data = {
        "regNo": regno
    }
    response = requests.get(url, headers=headers, data=data)

    return Response(response.json())