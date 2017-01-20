from flask import Flask, abort, flash, redirect, render_template, session, url_for, request
from flask.ext.qrcode import QRcode

from os import urandom, path, getpid
from binascii import hexlify
import inspect
import logging

import requests as req

import json


def run():
    flask_options = dict(port=PORT, host='0.0.0.0', debug=True)
    app.secret_key = hexlify(urandom(24))
    app.run(**flask_options)


def save_pid():
    """Save pid into a file: filename.pid."""
    pidfilename = inspect.getfile(inspect.currentframe()) + ".pid"
    f = open(pidfilename, 'w')
    f.write(str(getpid()))
    f.close()


def generate_url(host, protocol='http', port=80, directory=''):

    if isinstance(directory, list):
        directory = '/'.join(directory)

    return "%s://%s:%d/%s" % (protocol, host, port, directory)


app = Flask(__name__, static_url_path="", static_folder='static')
QRcode(app)

MY_IP = req.get(generate_url('jsonip.com')).json()['ip']
PORT = 88


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html', about_url=generate_url(MY_IP, port=PORT, directory=url_for('about')[1:]))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

"""
@app.route('/api/count-terms', methods=['POST'])
def api_count_terms():
    return json.dumps()
"""

if __name__ == '__main__':

    save_pid()

    logfilename = inspect.getfile(inspect.currentframe()) + ".log"
    logging.basicConfig(filename=logfilename, level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Started")

    run()
