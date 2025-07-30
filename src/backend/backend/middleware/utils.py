import requests
import socket
from requests import get
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
    send_discord_alert(
            channel_url=settings.DISCORD_EBARIMT_CHANNEL_URL,
            msg=data
        )
    if data.get("status") == 200:
        return data.get('data')
    return None


def send_discord_alert(channel_url, msg):
    data = {'content': msg}
    try:
        res = requests.post(
            url=channel_url,
            headers={
                'Content-type': 'application/json',
                'User-Agent': 'ZeroTech POS-Backend'
            },
            json=data
        )
        if res.status_code not in range(200, 299):
            return
    except:
        return False

def get_address():
    remote_address=None
    ip = get('https://api.ipify.org').text
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect((ip, 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = remote_address
    finally:
        s.close()
    return IP