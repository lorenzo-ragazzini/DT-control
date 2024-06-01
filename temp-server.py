import asyncio
import threading
import time
import requests
from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.implementation.cloud.cloud import download
from waitress import serve
import json
import subprocess

if __name__ == "__main__":
    port = 80
    app.dt = DigitalTwin()
    print("Digital Twin server started on port %s"%port)
    with open('config.json') as f:
        input_path = json.load(f)['input_path']
        print("input path: %s"%input_path)
    threading.Thread(target=download,args=('WorkInProcess.txt',input_path,'dt-input/',5)).start()
    try:
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", "ngrok", "http", str(port)])
        time.sleep(5) # wait for ngrok to start
        response = requests.get('http://localhost:4040/api/tunnels')
        print("ngrok tunnel to the digital twin is open")
        print("pubblic address: %s"%response.json()["tunnels"][0]["public_url"])
        print("access code: %s"%response.json()["tunnels"][0]["public_url"].split("://")[1].split("-")[0])
    except:
        print("cannot detect the ngrok address")
    serve(app, host='127.0.0.1', port=port, expose_tracebacks=True, threads=8)

# the address is available at: (account Google @polimi)
# https://dashboard.ngrok.com/cloud-edge/endpoints
    
# api key: 2bjC06hzYIGYU6JXLeMaFByjLAL_34xbAoZM7S7XYjup2Y7tm
# token 2YwwqqdkgiysCtMBJIY5slj6h9y_3Mgs6keY1Q8qq4tzPnDnw
