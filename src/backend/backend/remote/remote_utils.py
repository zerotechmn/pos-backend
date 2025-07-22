import websocket
import socket

def create_websocket(local_ip, ws_url):
    def custom_socket(*args, **kwargs):
        sock = socket.create_connection((host, port), timeout=10, source_address=(local_ip, 0))
        return sock

    from urllib.parse import urlparse
    parsed_url = urlparse(ws_url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == "wss" else 80)

    ws = websocket.WebSocket()
    ws.connect(ws_url,
               sockopt=None,
               socket=custom_socket())
    
    ws.send("Hello from " + local_ip)
    print(ws.recv())
    ws.close()

local_ip = "192.168.1.100"
ws_url = "ws://echo.websocket.org"
create_websocket(local_ip, ws_url)
