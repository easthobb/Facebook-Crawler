import flask
import json
import os
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import urllib.request
import requests


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
    return """
    <a href="/fb-login">Login for get token</a>
    <a href="/fb-crawling">Do Crawling </a>
    """

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
    User information: <br>
    Name: {name} <br>
    Email: {email} <br>
    img: <img src="{picture_url}"> <br>
    <a href="/">Home</a>
    <input id="submitbutton" type="submit" name="submitbutton" value="run"/>
	
    """
    
@app.route("/fb-crawling")
def crawling():
    
    #크롤링 함수 매개변수 
    # [ page_id(str) , post_type(str), post_text(str), post_shares(int), post_comments(int), post_reaction_total, LIKE,LOVE,...]
    # page-id -> post_id, post_txt, post_type, total_reactions

    # post-id ->  shares, post_comments,
    # 
    # post - reactions
    # ?fields=attachments,reactions.summary(total_count)
    # 124691830975231/posts?fields=comments.summary(total_count),shares,reaction.summary(total_count)

    long_token = get_long_token()

    
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

    
select_one('#list_subject_7854731 > font.mobile_hide')
        

    return """
    THANKS.
    """

if __name__ == "__main__":
    app.run(debug=True)