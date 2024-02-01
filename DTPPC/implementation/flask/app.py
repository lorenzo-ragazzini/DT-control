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
    DTname = app.dt.new()
    print('Creating DT instance: %s' %DTname)
    return DTname
    
@app.route('/clear',methods=['POST'])
def clear():
    DTname = request.json['name']
    print('Clearing DT instance: %s' %DTname)
    return app.dt.clear(DTname)
    
@app.route('/run',methods=['GET','POST'])
def run():
    input = json.loads(request.json)
    name = input.pop('name')
    print("Executing request %s on DT %s"%(input,name))
    if request.method == 'POST':
        app.results[name] = app.dt[name].interface(**input)
        return app.results[name]
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

