import asyncio
from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.implementation.cloud.cloud import download
from waitress import serve
import json
  
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.dt = DigitalTwin()
    with open('config.json') as f:
        input_path = json.load(f)['input_path']
    asyncio.run(download('Running_Orders.xlsx',input_path,'dt-input/',5))
    serve(app, host='127.0.0.1', port=5000)