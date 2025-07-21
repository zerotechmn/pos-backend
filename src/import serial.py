import serial
import requests
import time
import json
from datetime import datetime

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
API_URL = 'http://localhost:27028'

def main():
    print("Log message", flush=True)
    print("Serial forwarder service started.", flush=True)
    GlSerialPort = None

    try:
        GlSerialPort = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
        print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud rate...", flush=True)
        print("is_open .... ", GlSerialPort.is_open, flush=True)
        
        while True:
            waiting = GlSerialPort.in_waiting
            if waiting > 0:
                line = GlSerialPort.readline()
                print(f"Received from serial: {line}", flush=True)

                str_line = line.decode('utf-8').strip()
                print(f"Received from serial str: {str_line}", flush=True)
                if str_line == "sale":
                    db_ref_no = datetime.now().strftime("%Y%m%d%H%M%S")
                    payload = {
                        "service_name": "doSaleTransaction",
                        "service_params": {
                            "db_ref_no": db_ref_no,
                            "amount": "1500"
                        }
                    }

                    try:
                        response = requests.post(API_URL, json=payload, timeout=60)
                        if response.status_code == 200:
                            reply = response.json()
                            if reply.get("response"):
                                ret = reply.get("response")
                                if ret.get('response_code') == "000":
                                    reply = str(response.json())
                        else:
                            reply = f"Error: {response.status_code}"

                    except requests.RequestException as e:
                        reply = f"Request error: {str(e)}"

                    print(f"Response from serial str: {reply}", flush=True)
                    # GlSerialPort.write((reply + '\n').encode('utf-8'))
                    if isinstance(reply, (dict, list)):
                        response_data = json.dumps(reply).encode('utf-8')
                    elif isinstance(reply, bytes):
                        response_data = reply
                    else:
                        response_data = str(reply).encode('utf-8')
                    response_data += b'\n'
                    print(f"Sent to serial: {response_data}", flush=True)

                    try:
                        written = GlSerialPort.write(response_data)
                        print(f"Wrote {written} bytes to serial port", flush=True)
                    except serial.SerialException as e:
                        print(f"Serial write error: {e}", flush=True)

            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Serial error: {e}", flush=True)

    finally:
        if GlSerialPort and GlSerialPort.is_open:
            print("Closing serial port...", flush=True)
            GlSerialPort.close()

if __name__ == "__main__":
    main()