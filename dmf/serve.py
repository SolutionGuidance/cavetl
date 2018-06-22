from flask import Flask, Response, jsonify
from json import dumps
from api_client.veris import VerisSsnClient as SsnClient
import requests
import pdb

app = Flask(__name__)
try:
    app.config.from_envvar('DMF_CONFIG')
except RuntimeError:
    app.config.from_object('config')


client = SsnClient(
    user_id=app.config['USER_ID'],
    password=app.config['PASSWORD'],
    http_proxy=app.config['HTTP_PROXY'],
    https_proxy=app.config['HTTPS_PROXY']
)

@app.route('/')
def index():
    return 'hello world'

@app.route('/ssn/<ssn>')
def dmf_search(ssn):
    xml = client.getDmfRecord(ssn)
    return Response(dumps(xml), content_type="application/json")

if __name__ == '__main__':
    app.run(debug=True)
