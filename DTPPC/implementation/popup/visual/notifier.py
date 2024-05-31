from flask import Flask, render_template, request, redirect, url_for, g
import requests
import multiprocessing

logger = Flask(__name__)
# app.items = ["Item 1", "Item 2", "Item 3"]
logger.items = list()

@logger.route('/')
def home():
    print(logger.items)
    return render_template('index.html', items=reversed(logger.items))

@logger.route('/post', methods=['POST'])
def post():
    item = request.form.get('item')
    logger.items.append(item)
    return redirect(url_for('home'))

def notify(item):
    response = requests.post('http://localhost:5000/post', data={'item': item})
    return response.status_code

if __name__ != '__main__':
    process = multiprocessing.Process(target=logger.run, kwargs={'debug': True})
    process.start()

if __name__ == '__main__':
    logger.run(debug=True)
    
    