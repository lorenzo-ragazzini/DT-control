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
    with open('config.json') as f:
        input_path = json.load(f)['input_path']
    # asyncio.run(download('Running_Orders.xlsx',input_path,'dt-input/',5))
    ngrok_process = subprocess.Popen(f'{"C:/Users/Lorenzo/Downloads/ngrok.exe"} http 5000', shell=True, close_fds=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # webbrowser.open()
    print(ngrok_process)
    serve(app, host='127.0.0.1', port=5000, expose_tracebacks=True)