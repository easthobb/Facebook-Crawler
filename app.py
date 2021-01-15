import flask
from flask import Flask, render_template,request,send_from_directory,abort
import json
import os
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import urllib.request
import requests
import fb_crawling
from fb_token import *
###################################################################

### BASIC SETTING
URL = "http://localhost:5000"

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
### 사용자가 첫번째로 보는 페이지 - 장기토큰 발급, URL 입력 후 크롤링 개시
@app.route("/")
def index():
    return render_template('index.html')

####################################################################
### Facebook session 로그인 후 토큰 교환 
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
    
    return f"""
    TOKEN REFRESHED, 
	
    """
    
@app.route("/fb-crawling",methods=['POST'])
def crawling():
    
    full_URL = request.form['url']
    
    ##URL 분해
    page_name = full_URL.split('facebook')[1].split('/')[1]

    ## 크롤러 객체 생성 및 실행
    crawler = fb_crawling.Facebook_Crawler(page_name)
    crawler.start()
    
    ## 파일 클라이언트로 전송
    filename = page_name + '.csv'
    try:
        return send_from_directory('./', filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    
    return flask.redirect('/')


if __name__ == "__main__":
    app.run(debug=True)