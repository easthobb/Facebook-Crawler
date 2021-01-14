import json, os

def get_appid():
    with open('app_id.json','r') as id:
        app_id = json.load(id)
        app_id = app_id['app_id']
    return app_id

def get_secret():
    with open('app_secret.json','r') as sec:
        app_secret = json.load(sec)
        app_secret = app_secret['app_secret']
    return app_secret

def set_long_token(token):
    long_token=dict()
    long_token['token'] = token
    with open('long_token.json','w') as t:
        json.dump(long_token,t)

def set_app_token(token):
    app_token=dict()
    app_token['token'] = token
    with open('app_token.json','w') as t:
        json.dump(app_token,t)

def get_long_token():
    with open('long_token.json','r') as long:
        long_token = json.load(long)
        long_token = long_token['token']
    return long_token

def get_app_token():
    with open('app_token.json','r') as app:
        app_token = json.load(app)
        app_token = app_token['token']
    return app_token