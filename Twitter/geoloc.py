import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
Not_found = {'status':404, 'message':"tweets not found"}

auth = tweepy.OAuthHandler(os.getenv('TW_API'),os.getenv('TW_API_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'),os.getenv('ACCESS_TOKEN_SEC'))

api =tweepy.API(auth)


def getbygeo(lat,lon,rad):

    if(lat=='' or lon == '' or rad==''):
        Not_found,404
        

    try:
        #print(f'{lat},{lon},{rad} km')
        searched = api.search_tweets(q="",geocode=f"{lat},{lon},{rad}km")

        max_tweets = 10
        output = []
        for i in range(len(searched)):
            dic = {}
            dic['text'] = searched[i].text
            dic['user_screen_name'] = searched[i].user.screen_name
            output.append(dic)

            if i == max_tweets:
                break

            i+=1

        return f'{output}',200
        

    except:
        return Not_found,404



    