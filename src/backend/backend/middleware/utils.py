import requests
from django.conf import *
from backend.base.models import User


def UserCreate(data):
    user = User.objects.filter(username=data.get("username")).first()
    print("token data : ", data)
    if not user:
        user = User()
        user.username = data.get("username")
        user.token_password = data.get("password")
        user.save()
    url = settings.GUUR_URL + "/api/auth/get_tokens"
    params = {'username': user.username, 'password': user.token_password}
    response = requests.get(url, params=params)
    return response

def getToken():
    user = User.objects.filter().first()
    url = settings.GUUR_URL + "/api/auth/get_tokens"
    params = {'username': user.username, 'password': user.token_password}
    print("token param : ", params)
    response = requests.get(url, params=params)
    return response.json()

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
    print("valid response ", response.json())
    data = response.json()
    if data.get("status") == 200:
        return data.get('data')
    return None