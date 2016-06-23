from flask import Flask, render_template, request
import uuid
import pika
from stock_tracer.common import MQClient

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('data.html')

@app.route('/add', methods=['POST'])
def add_stock():
    app.logger.info(request.form['exchange'])
    app.logger.info(request.form['symbol'])
    client = MQClient()
    request_body= {}
    request_body['action'] = 'add_stock'
    request_body['payload'] = {}
    request_body['payload']['exchange'] = request.form['exchange']
    request_body['payload']['symbol'] = request.form['symbol']
    app.logger.info(request_body)
    responce = client.call(request_body)

    return responce

if __name__ == "__main__":
    app.run()
