# Facebook-Crawler
This repository is for Facebook page crawlers. The Facebook crawler is based on Facebook Graph API 4.0. It can be execute by run the Web UI based on flask at a local server. The page URL is entered, crawls on the latest 100 posts on the page, and returns results in CSV (Changeable-post number and paging), which requires API tokens issued by the user directly registering the app, and works when saved as short-term and long-term token json files. Since code for exchanging short-term tokens for long-term tokens is implemented, it is recommended that short-term tokens be exchanged for long-term tokens before being used.

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

