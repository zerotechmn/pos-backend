import requests
from django.conf import *
from backend.base.models import User

def getToken():
    user = User.objects.filter().first()
    url = settings.GUUR_URL + "/api/auth/get_tokens"
    params = {'username': user.username, 'password': user.password}
    response = requests.get(url, params=params)
    return response