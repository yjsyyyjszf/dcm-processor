from flask import Flask, request, make_response
import logging
from worker import process_task
from threading import Thread

# start flask application
app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World."


@app.route('/stable-series', methods=['POST'])
def onStableSeries():
    data = request.get_json(force=True)
    thread = Thread(target=process_task, kwargs={'data': data})
    thread.start()
    return make_response({"status": "accepted"})
