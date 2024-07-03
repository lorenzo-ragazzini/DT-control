import warnings
from flask import Flask, render_template, request, redirect, url_for, g
import requests
from datetime import datetime

app = Flask(__name__)
# app.items = ["Item 1", "Item 2", "Item 3"]
app.items = list()

@app.route('/')
def home():
    print(app.items)
    return render_template('index.html', items=reversed(app.items))

@app.route('/post', methods=['POST'])
def post():
    item = request.form.get('item')
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    item = f"({current_time}) {item}"
    app.items.append(item)
    return redirect(url_for('home'))

def notify(title="", message="", app_name='DTPPC', timeout=5):
    if title and message:
        item = "%s: %s"%(title,message)
    else:
        item = title + message
    try:
        response = requests.post('http://localhost:5000/post', data={'item': item})
        return response.status_code
    except:
        print(item)
        warnings.warn("Cannot connect to the notification server")
        return 500

if __name__ == '__main__':
    app.run(debug=True)
    
    