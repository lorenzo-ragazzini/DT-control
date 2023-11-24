'''Flask backend for DT calls'''
from flask import Flask, request
from DTPPC.digitaltwin import DigitalTwin
from typing import Any
from waitress import serve
import requests
import json

app = Flask(__name__)
app.debug = True
app.dt : DigitalTwin = None
app.results : dict[str,Any] = dict()

@app.route('/new',methods=['GET'])
def new():
    return app.dt.new()
    
@app.route('/clear',methods=['POST'])
def clear():
    name = request.json['name']
    return app.dt.clear(name)
    
@app.route('/run',methods=['GET','POST'])
def run():
    input = json.loads(request.data.decode())
    name = input.pop('name')
    if request.method == 'POST':
        app.results[name] = app.dt.interface(**input)
    if request.method == 'GET':
        return app.results.pop(name)

@app.route('/synchronize',methods=['POST'])
def synchronize():
    pass

@app.route('/update',methods=['POST'])
def update():
    pass

def run_server():
    app.run()
    serve(app, host='127.0.0.1', port=5000)

