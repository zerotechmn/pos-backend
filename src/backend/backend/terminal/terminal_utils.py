import requests
from django.conf import *
from django.conf import settings
from backend.base.models import Terminal
from backend.middleware.utils import send_discord_alert

def CreateTerminal(data):
    terminal = Terminal.objects.filter(terminal_pos_no=data.get("pos_no")).first()
    print("terminal data : ", data)
    if not terminal:
        terminal = Terminal()
    terminal.terminal_pos_no = data.get("pos_no")
    terminal.name = data.get("name")
    terminal.terminal_id = data.get("terminal_id")
    terminal.mac_address = data.get("mac_address")
    terminal.ip_address = data.get("ip_address")
    terminal.guur_user = data.get("guur_user")
    terminal.guur_token = data.get("guur_token")
    terminal.application_version = data.get("application_version")
    terminal.tbd_application_version = data.get("tbd_application_version")
    terminal.tdb_terminal_id = data.get("tdb_terminal_id")
    terminal.pts_ip_address = data.get("pts_ip_address")
    terminal.save()
    
    send_discord_alert(
        channel_url=settings.DISCORD_SET_TERMINAL_CHANNEL_URL,
        msg="SET NEW TERMINAL. POS Number: %s" % (
            str(terminal.terminal_pos_no)
        )
    )

    return True
