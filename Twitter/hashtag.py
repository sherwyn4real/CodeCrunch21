import requests
import tweepy
import json

auth = tweepy.OAuthHandler('6e9HsAYRq63W3BRk1zViJNRRB', 'NYh34GyNpWtQLkfnBnDSmZHeF0no0yPeh6GAtyvcrx221DQaMJ')
auth.set_access_token('1263798218338504704-wNRSTbQ1IYyaL0SwzAiK8bJ0mWNMWq','wKBIjy1VPUsnNkovYU6ydBvsWRSeIxJh9RSRfWLQOEFFp')

api =tweepy.API(auth)

def getbyhashtag(htag):
    try:
        tweets = api.search_tweets(q="#{htag}")
        print(type(tweets))

    except:
        return
        
getbyhashtag("codeCrunch21")