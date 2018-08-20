from flask import Flask, Response, jsonify
from json import dumps
import requests
import pdb
import importlib

app = Flask(__name__)
try:
    app.config.from_envvar('DMF_CONFIG')
except RuntimeError:
    app.config.from_object('config')

try:
    SsnClient = getattr(importlib.import_module(app.config['SSN_MODULE']), app.config['SSN_CLIENT'])
except (ModuleNotFoundError, KeyError, AttributeError):
    raise ImportError("Your SSN client backend couldn't be imported, probably because of an error with configuration.")

client = SsnClient(app.config)

@app.route('/')
def index():
    return Response(status=200)

@app.route('/dmf/<ssn>')
def dmf_search(ssn):
    dmf_record = client.get_dmf_record(ssn)
    return Response(dumps(dmf_record), content_type="application/json")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
