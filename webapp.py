from flask import Flask, redirect, Markup, url_for, session, request, jsonify
from flask import render_template
from flask_oauthlib.client import OAuth
#from bson.objectid import ObjectId

import pprint
import os
import sys
#import pymongo
from datetime import datetime, date, timedelta
from pytz import timezone
import pytz

app = Flask(__name__)

@app.route('/') 
def render_login():
    return render_template('login.html')
                                                 
if __name__ == "__main__":
    app.run()
