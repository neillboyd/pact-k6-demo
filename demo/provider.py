#!/usr/env/bin python
import datetime
import json
import uuid

from flask import Flask, abort, jsonify, request

fakedb = {}

app = Flask(__name__)

@app.route('/_pact/provider_states', methods=['POST'])
def provider_states():
    mapping = {'UserA does not exist': setup_no_user_a,
               'UserA exists and is not an administrator': setup_user_a_nonadmin}
    mapping[request.json['state']]()
    return jsonify({'result': request.json['state']})


def setup_no_user_a():
    if 'UserA' in fakedb:
        del fakedb['UserA']


def setup_user_a_nonadmin():
    fakedb['UserA'] = {'name': "UserA", 'id': '98b6653c-9738-439b-a203-a7c6e8e20851', 'created_on': '2020-07-23T12:00:00', 'admin': False}

def setup_initial_user():
    fakedb['K6User'] = {'name': "K6User", 'id': '98b6653c-9738-439b-a203-a7c6e8e20851', 'created_on': '2020-07-23T12:00:00', 'admin': False}

@app.route('/users/<name>')
def get_user_by_name(name):
    user_data = fakedb.get(name)
    if not user_data:
        abort(404)
    response = jsonify(**user_data)
    app.logger.debug('get user for %s returns data:\n%s', name, response.data)
    return response


if __name__ == '__main__':
    setup_initial_user()
    app.run(debug=True, port=5001)
