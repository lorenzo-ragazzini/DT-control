import asyncio
from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.implementation.cloud.cloud import download
from waitress import serve
import json
import subprocess
import webbrowser
  
if __name__ == "__main__":
    app.dt = DigitalTwin()
    # with open('config.json') as f:
    #     input_path = json.load(f)['input_path']
    input_path = 'C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB'
    # asyncio.run(download('WorkInProcess.xlsx',input_path,'dt-input/',5))
    loop = asyncio.new_event_loop()
    asyncio.run_coroutine_threadsafe(download('WorkInProcess.txt',input_path,'dt-input/',5),loop)
    ngrok_process = subprocess.Popen(f'{"C:/Users/Lorenzo/Downloads/ngrok.exe"} http 5000', shell=True, close_fds=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # webbrowser.open()
    serve(app, host='127.0.0.1', port=5000, expose_tracebacks=True)

# the address is available at:
# https://dashboard.ngrok.com/cloud-edge/endpoints