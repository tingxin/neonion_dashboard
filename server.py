__author__ = 'tingxxu'
__copyright__ = "2015 Cisco Systems, Inc."

# !flask/bin/python
# run with flask
from flask import Flask, jsonify, Response, request, send_from_directory

import json
# import urllib
# import urlparse
# import os
from controller.application import Application

# create simple flask server
flaskInstance = Flask(__name__, static_url_path='')
app = Application()

# default handler
@flaskInstance.errorhandler(404)
def not_found(error):
    response = jsonify({'error': error.description})
    return response


@flaskInstance.route('/', methods=['GET'])
def index():
    print(request.query_string)
    return flaskInstance.send_static_file('index.html')


def send_css(path):
    return send_from_directory('static/css', path)

@flaskInstance.route('/script/<path:path>', methods=['GET'])
def send_script(path):
    return send_from_directory('static/script', path)

@flaskInstance.route('/node/<string:info>', methods=['POST', 'PUT'])
def post(info):
    app.receive(request.data)
    return Response("Hello,this is Neonion Gateway Service")


@flaskInstance.route('/api/data/<string:status_key>', methods=['GET'])
def get_data(status_key):
    result = app.get_data(status_key)
    if result is not None:
        data = json.dumps(result)
        response = Response(response=data, status=200, mimetype="application/json")
    else:
        response = Response(response={}, status=404, mimetype="application/json")
    return response

@flaskInstance.route('/api/all', methods=['GET'])
def get_all():
    result = app.get_all()
    if result is not None:
        data = json.dumps(result)
        response = Response(response=data, status=200, mimetype="application/json")
    else:
        response = Response(response={}, status=404, mimetype="application/json")
    return response


@flaskInstance.route('/api/diagnostics', methods=['GET'])
def get_diagnostics():
    result = app.get_diagnostics()
    if result is not None:
        data = json.dumps(result)
        response = Response(response=data, status=200, mimetype="application/json")
    else:
        response = Response(response={}, status=404, mimetype="application/json")
    return response


@flaskInstance.route('/api/history', methods=['POST', 'PUT'])
def get_history():
    parameter = request.json
    keys = parameter['keys']
    seconds = parameter['seconds']

    result = app.get_history(keys, seconds)
    if result is not None:
        data = json.dumps(result)
        response = Response(response=data, status=200, mimetype="application/json")
    else:
        response = Response(response={}, status=404, mimetype="application/json")
    return response


if __name__ == "__main__":

    local_ip = raw_input("--Please input local ip:\n")

    flaskInstance.run(debug=False, host=local_ip, port=5003)

    print('main thread finished!')
