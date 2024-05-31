import asyncio

import requests
from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.implementation.cloud.cloud import download
from waitress import serve
import json
import subprocess
import webbrowser
  
if __name__ == "__main__":
    print("DT server UP")
    port = 80
    app.dt = DigitalTwin()
    # with open('config.json') as f:
    #     input_path = json.load(f)['input_path']
    input_path = 'C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB'
    # asyncio.run(download('WorkInProcess.xlsx',input_path,'dt-input/',5))
    loop = asyncio.new_event_loop()
    asyncio.run_coroutine_threadsafe(download('WorkInProcess.txt',input_path,'dt-input/',5),loop)
    # can launch ngrok from here:
    if True:
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", "ngrok", "http", str(port)])
        response = requests.get('http://localhost:4040/api/tunnels')
        print("pubblic address: %s"%response.json()["tunnels"][0]["public_url"])
        print("access code: %s"%response.json()["tunnels"][0]["public_url"].split("://")[1].split("-")[0])
    serve(app, host='127.0.0.1', port=port, expose_tracebacks=True, threads=8)

# the address is available at: (account Google @polimi)
# https://dashboard.ngrok.com/cloud-edge/endpoints
    
# api key: 2bjC06hzYIGYU6JXLeMaFByjLAL_34xbAoZM7S7XYjup2Y7tm
# token 2YwwqqdkgiysCtMBJIY5slj6h9y_3Mgs6keY1Q8qq4tzPnDnw
