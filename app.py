import flask
import json
import os
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import urllib.request
import requests

### BASIC SETTING
URL = "http://localhost:5000"


## KEY SETTING
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
    
## FB OBJECT SETTING
FB_CLIENT_ID = get_appid()
FB_CLIENT_SECRET = get_secret()
FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FB_SCOPE = ["email"]

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)

###################################################################
@app.route("/")
def index():
    return """
    <a href="/fb-login">Login for get token</a>
    <a href="/fb-crawling">Do Crawling </a>
    """


@app.route("/fb-login")
def login():
    
    ## Facebook Object loads
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

    return flask.redirect(authorization_url)


@app.route("/fb-callback")
def callback():
    ##facebook OAuth session setting
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    ## we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    ## SHORT TOKEN SETTING FOR TOKEN EXCHANGE
    short_token = facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=flask.request.url,
    )
    short_token=short_token['access_token']
    print("SHORT TOKEN:",short_token)

    # Fetch a protected resource, i.e. user profile, via Graph API
    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data["email"]
    name = facebook_user_data["name"]
    picture_url = facebook_user_data.get("picture", {}).get("data", {}).get("url")

    ## GETTING LONG TOKEN
    long_token = facebook.get(
         f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={FB_CLIENT_ID}&client_secret={FB_CLIENT_SECRET}&fb_exchange_token={short_token}"
    ).json()
    long_token=long_token['access_token']
    set_long_token(long_token)
    print("LONG TOKEN:",long_token)
    

    ## GETTING APP TOKEN
    app_token = facebook.get(
        f"https://graph.facebook.com/oauth/access_token?client_id={FB_CLIENT_ID}&client_secret={FB_CLIENT_SECRET}&grant_type=client_credentials").json()
    
    app_token=app_token['access_token']
    set_app_token(app_token)
    print("app_token: ",app_token)
    
    
    # page_request=f"https://graph.facebook.com/v4.0/2371586546315740/posts/?access_token={app_token}"
    # page_request_get=facebook.get(
    #      page_request
    #  ).json()
    # print(page_request_get)

    return f"""
    User information: <br>
    Name: {name} <br>
    Email: {email} <br>
    img: <img src="{picture_url}"> <br>
    <a href="/">Home</a>
    <input id="submitbutton" type="submit" name="submitbutton" value="run"/>
	
    """
    # @app.route('/fb-longterm')
    # def getLongToken():
    #     face

@app.route("/fb-crawling")
def crawling():
    
    ##facebook OAuth session setting
    # facebook = requests_oauthlib.OAuth2Session(
    #     FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL
    # )

    # ## we need to apply a fix for Facebook here
    # facebook = facebook_compliance_fix(facebook)
    long_token = get_long_token()
    # page_request=f"https://graph.facebook.com/v4.0/2371586546315740/posts/?access_token={app_token}"
    # page_request_get=facebook.get(
    #      page_request
    #  ).json()
    # print(page_request_get)

    ## 컨텐츠 확인
    data = requests.get(f"https://graph.facebook.com/v4.0/JTBClove/posts/?access_token={long_token}")
    total = requests.get(f"https://graph.facebook.com/v4.0/124691830975231/posts?limit=10&fields=reactions.summary(total_count)")
    print(data.json())
    data = data.json()
    for i in range(10):
        print("#####",data["data"][i]["message"])
        ## 작성 시간
        print("#####",data["data"][i]["created_time"])
        id = data["data"][i]["id"]
        print(total.json()["data"])

        

        

    return """
    THANKS.
    """

if __name__ == "__main__":
    app.run(debug=True)