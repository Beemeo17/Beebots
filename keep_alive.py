import logging
from flask import Flask, render_template
from threading import Thread
import datetime

app = Flask(__name__)
start_time = datetime.datetime.now()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    current_time = datetime.datetime.now()
    uptime = current_time - start_time
    hours = uptime.seconds // 3600
    return render_template('index.html', uptime=hours)


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
