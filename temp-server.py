from DTPPC.implementation.flask.app import app
from DTPPC.digitaltwin import DigitalTwin
from waitress import serve

    
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.dt = DigitalTwin()
    serve(app, host='127.0.0.1', port=5000)