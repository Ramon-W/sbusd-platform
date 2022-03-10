from flask_socketio import SocketIO, emit, join_room

import json
import os

from flask import Flask, redirect, Markup, url_for, session, request, jsonify
from flask import render_template

from oauthlib.oauth2 import WebApplicationClient
import requests

from bson.objectid import ObjectId

#import pprint
#import sys
import pymongo
#from datetime import datetime, date, timedelta
#from pytz import timezone
#import pytz

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_DISCOVERY_URL = (
    'https://accounts.google.com/.well-known/openid-configuration'
)

connection_string = os.environ['MONGO_CONNECTION_STRING']
db_name = os.environ['MONGO_DBNAME']
client = pymongo.MongoClient(connection_string)
db = client[db_name]
collection = db['Users']

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

socketio = SocketIO(app, async_mode='gevent')

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route('/') 
def render_login():
    if request.args.get('error') != None:
        return render_template('login.html', login_error = request.args.get('error'))
    return render_template('login.html')

@app.route('/login')
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
        prompt='consent'
    )
    return redirect(request_uri)

@app.route('/login/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']
    
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['name']
        if not users_email.endswith('@my.sbunified.org') and not users_email.endswith('@sbunified.org'):
            return redirect(url_for('render_login', error = "Please use your school issued email"))
    else:
        return redirect(url_for('render_login', error = "Email not available or verified"))
    session['unique_id'] = unique_id
    session['users_email'] = users_email
    session['picture'] = picture
    session['users_name'] = users_name
    if not collection.count_documents({ '_id': unique_id}, limit = 1):
        collection.insert_one({'_id': unique_id, 'name': users_name, 'email': users_email, 'picture': picture})
    return redirect(url_for('render_main_page'))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json() #handle errors to google api call
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('render_login'))

@socketio.on('connect')
def connect():
    socketio.emit('join_room_announcement', {'username': 'bob', 'room': '1'})

@socketio.on('join_room')
def join(data):
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)
    
@app.route('/sbhs')
def render_main_page():
    return render_template('index.html', username = session['users_name'], room = '1')

if __name__ == '__main__':
    socketio.run(app, debug=True)
