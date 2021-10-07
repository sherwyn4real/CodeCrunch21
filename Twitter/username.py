import tweepy
import os
from dotenv import load_dotenv


load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TW_API'),os.getenv('TW_API_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'),os.getenv('ACCESS_TOKEN_SEC'))

api =tweepy.API(auth)

def getbyusername(uname):
    try:

        user = api.get_user(screen_name=uname)
        user_timeline = tweepy.Cursor(api.user_timeline,screen_name=uname)
    

    except:
        return { "status": 404, "message":"tweets not found"}


    output = {}
    output['user_name'] = user.name
    output['user_screen_name'] = user.screen_name
    output['followers_count'] = user.followers_count
    output['friends_count'] = user.friends_count
    output['tweets'] = []
    
    
    for status in user_timeline.items(10):
        output['tweets'].append({'created_at':str(status.created_at), 'text':status.text})

    return output,200

