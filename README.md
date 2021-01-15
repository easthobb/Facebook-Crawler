# Facebook-Crawler
이 레포지토리는 페이스북 페이지 크롤러를 위한 레포지토리이다. 이 페이스북 크롤러는 페이스북 Graph API 4.0에 기반한다. 플라스크를 통해 로컬 서버에서 웹 UI를 띄워 동작이 가능하다. 페이지 URL을 입력받아 해당 페이지에 대한 최신 100개 정도의 게시물에 대해 크롤링을 수행하며 CSV로 결과를 반환한다.(변경 가능) 본 크롤러의 동작에는 사용자가 직접 앱 등록을 거쳐 발급받은 API 토큰이 필요하며 단기, 장기 토큰 json 파일로 저장 시 동작한다. 단기 토큰을 장기 토큰으로 교환할 수 있는 코드가 구현되어 있으므로, 단기 토큰을 장기 토큰으로 교환 후 사용할 것을 권한다. 

## Have to Prepare

    Facebook App id : app_id.json
    Facebook Access Token : long_token.json # doesn't matter long or short, but needs PPCA  

## Requirements

- have to get public page's latest post(default:100)
- have to save each post's 
    - title
    - published_time
    - type of contents
    - number of comments
    - number of contents
    - each reactions(ex like, love, haha,...)


## Usage
    #install dependcy
    pip3 install -r requirements.txt
    
    #flask run
    flask run -p 5000

## Execution
![ui](https://user-images.githubusercontent.com/57410044/104693306-c5a52e80-574c-11eb-96c3-e4155d5ac92d.png)
![runlog](https://user-images.githubusercontent.com/57410044/104693316-c938b580-574c-11eb-9eea-c6dfd036b76c.png)
![result](https://user-images.githubusercontent.com/57410044/104693330-cc33a600-574c-11eb-84db-68881a6c3361.png)

