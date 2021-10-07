import tweepy
import os
import json
from dotenv import load_dotenv

load_dotenv()
auth = tweepy.OAuthHandler(os.getenv('TW_API'),os.getenv('TW_API_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'),os.getenv('ACCESS_TOKEN_SEC'))

api =tweepy.API(auth)

def getbyhashtag(htag):
        try:
                tweets = api.search_tweets(q=f"#{htag}")
                max_tweets = 9
                output = []
                print("len=",len(tweets))
                for i in range(len(tweets)):
                        dic={}
                        status = tweets[i]

                        dic['text'] =status.text
                        dic['user_screen_name'] =status.user.screen_name
                        dic['retweet_count'] =status.retweet_count
                        output.append(dic)

                        if i==max_tweets:
                                print(i)
                                break
                        i+=1
                return f'{output}',200

        except:
                return { "status": 404, "message":"tweets not found"},404


