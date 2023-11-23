from DTPPC.implementation.flask.app import app
from waitress import serve

    
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    serve(app, host='0.0.0.0', port=5000)