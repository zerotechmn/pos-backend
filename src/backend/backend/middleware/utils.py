import requests
from django.conf import *
from backend.base.models import User

def getToken():
    user = User.objects.filter().first()
    url = settings.GUUR_URL + "/api/auth/get_tokens"
    params = {'username': user.username, 'password': user.password}
    response = requests.get(url, params=params)
    return response

def getMerchantTin(regno):
    if regno in [None, ""]:
        return None
    print("valid regno ", regno)
    url = "https://api.ebarimt.mn/api/info/check/getTinInfo"
    headers = {"Accept": "application/json"}
    data = {
        "regNo": regno
    }
    response = requests.get(url, headers=headers, data=data)
    print("valid response ", response)
    return response.json()