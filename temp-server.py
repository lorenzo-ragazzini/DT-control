from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.implementation.cloud.cloud import download
from waitress import serve
import json


    
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.dt = DigitalTwin()
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    download('Running_Orders.xlsx',input_path,'dt-input/')
    serve(app, host='127.0.0.1', port=5000)