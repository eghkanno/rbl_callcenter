from flask import Flask, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timezone, timedelta
from google.cloud import datastore

# config
config = json.load(open('config.json', 'r'))
path = config["path"]
users = config["users"]
JST = timezone(timedelta(hours=+9), 'JST')

# auth
auth = HTTPBasicAuth()
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# Datastore
datastore_client = datastore.Client()
kind='rbl_data'
name='latest_call'
key = datastore_client.key(kind, name)
entity = datastore.Entity(key)

def update_latest_call(dt):
    entity = datastore.Entity(key)
    entity.update({
        'timestamp': dt
    })
    datastore_client.put(entity)

def get_latest_call_time():
    latest_call = datastore_client.get(key)
    timestamp = latest_call['timestamp']
    return timestamp

# run if no entity hes been created yet
latest_call = datastore_client.get(key)
if latest_call == None:
    now = datetime.now(JST)
    update_latest_call(now)

app = Flask(__name__)
@app.route(path, methods=['GET', 'POST'])
@auth.login_required
def callcenter():
    if request.method == 'GET':
        res = jsonify({
            'latest_call_time': get_latest_call_time()
            })
    if request.method == 'POST':
        now = datetime.now(JST)
        update_latest_call(now)
        res = 'alert accepted.'
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)