import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import calendar

load_dotenv()

url = "https://api.nasa.gov/planetary/apod"

currentMonth = datetime.now().month
currentYear = datetime.now().year
currentDay = datetime.now().day

#get image of the first day of month of current date
def getimage():
    params = {
            'date':f'{currentYear}-{currentMonth}-01',
            'api_key':os.getenv('NASA_APIKEY')
    }

    r = requests.get(url,params=params)
    if r.status_code in (200,202):
        data = r.json()

        output = {
            "date":data["date"],
            "media_type":data["media_type"],
            "title":data["title"],
            "url": data["url"]
        }

        return output,200

    else:
        return {"status":404, 'message':'image not found'},r.status_code


#Get images in a month

def getimages(year,m):

    month = list(calendar.month_name).index(m) #returns month number
        
    
        #return {"status":404, "message":'Image not found'}

    if int(year) == currentYear and month == currentMonth:
        days = currentDay
        

    else:
        y = int(year)
        l = list(calendar.monthrange(y,month))
        days = l[1]

    params = {
        "start_date": f'{year}-{month}-01',
        "end_date": f'{year}-{month}-{days}',
        'api_key': os.getenv('NASA_APIKEY')
    }


    r = requests.get(url,params = params)
    
    if r.status_code in (200,202):
        data = r.json()
        output = []
        for i in range(len(data)):
            if data[i]['media_type'] == 'image':
                output.append(data[i]['url'])

        return f'{output}',200

    else:
        return {"status":404, 'message':'images not found'},404


#get videos

def getvideos(year,m):
    month = list(calendar.month_name).index(m) #returns month number

    if int(year) == currentYear and month == currentMonth:
        days = currentDay
        

    else:
        y = int(year)
        l = list(calendar.monthrange(y,month))
        days = l[1]

    params = {
        "start_date": f'{year}-{month}-01',
        "end_date": f'{year}-{month}-{days}',
        'api_key': os.getenv('NASA_APIKEY')
    }


    r = requests.get(url,params = params)
    
    if r.status_code in (200,202):
        data = r.json()
        output = []
        for i in range(len(data)):
            if data[i]['media_type'] == 'video':
                output.append(data[i]['url'])

        return f'{output}',200

    else:
        return {"status":404, 'message':'video not found'},404

#get epic

def getepic(dt):
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{dt}'  #2019-05-30?api_key=DEMO_KEY

    params = { 'api_key': os.getenv('NASA_APIKEY')
                }

    r = requests.get(url, params = params)
    
    
    if r.status_code in (200,202):
        data = r.json()
        output=[]

        for i in range(len(data)):
            dic={}
            lat = data[i]['centroid_coordinates']['lat']
            lon = data[i]['centroid_coordinates']['lon']
            if  lat >=10 and lat<=40 and lon>=120 and lon<=160:
                dic['identifier']= data[i]['identifier']
                dic['caption']= data[i]['caption']
                dic['image']= data[i]['image']
                dic['latitude'] =  lat
                dic['longitude'] =  lon
                output.append(dic)


        return f'{output}'

    else:
        return {"status":404, 'message':'image/video not found'},404

