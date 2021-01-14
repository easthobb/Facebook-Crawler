import requests
import os
import json
import csv
from fb_token import *


class Facebook_Crawler(object):

    def __init__(self):
        print("token init...")
        self.token = get_long_token()
        self.id = "JTBClove"  # crawled id for testing
        self.data_list=[]
    # Creating URL for crawling
    def create_URL(self, token, id):

        BASE_URL = "https://graph.facebook.com/v4.0/"

        query_piece = [
            'created_time', 'attachments', 'comments.summary(total_count)', 'shares', 'reactions.type(LIKE).limit(0).summary(true).as(like)',
            'reactions.type(LOVE).limit(0).summary(true).as(love)',
            'reactions.type(WOW).limit(0).summary(true).as(wow)',
            'reactions.type(HAHA).limit(0).summary(true).as(haha)',
            'reactions.type(SAD).limit(0).summary(true).as(sad)',
            'reactions.type(ANGRY).limit(0).summary(true).as(angry)',
            'reactions.type(THANKFUL).limit(0).summary(true).as(thankful)'
        ]

        full_query = BASE_URL + id + "/posts?limit=10&fields="  # for test limit 1
        full_query = full_query + ",".join(query_piece)
        full_query = full_query + f"&access_token={token}"

        return full_query

    # request_URL
    def request_URL(self, URL):

        try:
            # getting link from FACEBOOK API
            response = requests.get(URL)
            # logging
            print("request_URL : got response", response)
            # from response extract next page
            ## page 끝에 도달하면 next 없음..!!
            if 'next' in response.json()['paging']:
                next_page_link = response.json()['paging']['next']
            else:
                next_page_link = None

        except:
            print("request_URL : some error occured!")

        # tuple로 반환
        return response.json(), next_page_link

    # 단일 페이지로부터 필요한 정보 parse
    def parse_json(self, page_json):

        page_data_list = []
        page_json['data']
        
        for post in page_json['data']:
            post_created_time = post['created_time']
            # post 없는 경우 예외처리
            if 'title' in post['attachments']['data'][0]:
                post_title= post['attachments']['data'][0]['title']  # title
            else:
                post_title= post['attachments']['data'][0]['description']  # post_title

            post_type = post['attachments']['data'][0]['type']  # type
            # number of comments
            print(post['comments']['summary']['total_count'])
            if 'shares' in post:
                post_shares = post['shares']['count']  # number of shares
            else:
                post_shares = 0
            post_like = post['like']['summary']['total_count']
            post_love = post['love']['summary']['total_count']
            post_wow = post['wow']['summary']['total_count']
            post_haha = post['haha']['summary']['total_count']
            post_sad = post['sad']['summary']['total_count']
            post_angry = post['angry']['summary']['total_count']
            post_thankful = post['thankful']['summary']['total_count']
            data = [post_created_time, post_title, post_type, post_shares, post_like,
                    post_love, post_wow, post_haha, post_sad, post_angry, post_thankful]
            page_data_list.append(data)
        print(page_data_list)
        return page_data_list
        
    ## 페이지에서 얻어온 데이터 리스트를 병합하는 함수
    def combine_data_list(self,data_list,page_date_list):
        data_list = data_list + page_date_list
        return data_list

    ## 최종적으로 생성된 데이터 리스트에 대해 CSV로 전환해주는 함수
    def convert_to_csv(self, id, data_list):
        
        with open('./result.csv', 'w', encoding='utf-8-sig', newline='') as f:
             writer = csv.writer(f)
             writer.writerow(['post_created_time','post_title','post_type','post_shares','post_like','post_love','post_wow','post_haha','post_angry','post_sad','post_angry','post_thankful'])
             for data in enumerate(data_list):
                 if(data_list[0]<=100):
                     writer.writerow(data_list[1])
        
    
    def start(self):
        
        URL = self.create_URL(self.token, self.id)
        print("requesting :",URL)

        #처음 페이지에 대해 request
        response, next_page_link = self.request_URL(URL)
        print("link : ",next_page_link)
        json_listed = self.parse_json(response)
        data_list =self.combine_data_list(self.data_list,json_listed)

        while True :
            # 다음 페이지 유효성 검사
            if (next_page_link != None)and(len(data_list)<=30):
                print("next..page...")
                response,next_page_link = self.request_URL(next_page_link)
                json_listed = self.parse_json(response)
                data_list = self.combine_data_list(data_list,json_listed)
            else:
                break
            
        self.convert_to_csv("test",data_list)
        

if __name__ == "__main__":
    Facebook_Crawler = Facebook_Crawler()
    Facebook_Crawler.start()
