import requests
import os

KEY = os.getenv('WEAT_API_KEY') #api key



report_error = {
    "status": 404,
    "message": "weather data not found"
}

def search_city(cname):
 
    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cname}&APPID={KEY}&units=metric'
    response = requests.get(url).json()

    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        return report_error,404
    else:
        output={
            "country":response["sys"]["country"],
            "name":response["name"],
            "temp":response["main"]["temp"]
            }
        return output,200
     
       
 #========================================================================


def search_cord_pin(l):
    
    if(type(l) == list):
        url=f'http://api.openweathermap.org/data/2.5/weather?lat={l[0]}&lon={l[1]}&appid={KEY}&units=metric'
        response = requests.get(url)
        if response.status_code in (200,202):
            res = response.json()
            output={
            "country":res["sys"]["country"],
            "name":res["name"],
            "temp":res["main"]["temp"],
            "min_temp": res["main"]["temp_min"],
            "max_temp": res["main"]["temp_max"],
            "latitude":res["coord"]["lat"],
            "longitude": res["coord"]["lon"]
            }
            
            return output,200
            
        elif response.status_code == 400:
            return {'status':response.status_code, 'message':'Bad request'}
        else:
           return report_error,response.status_code
        
        
        '''if(type(l) == list):
        url=f'http://api.openweathermap.org/data/2.5/weather?lat={l[0]}&lon={l[1]}&appid={KEY}&units=metric'
        response = requests.get(url).json()
        if response.get('cod') != 200:
            return report_error,404
        
        else:
            output={
            "country":response["sys"]["country"],
            "name":response["name"],
            "temp":response["main"]["temp"],
            "min_temp": response["main"]["temp_min"],
            "max_temp": response["main"]["temp_max"],
            "latitude":response["coord"]["lat"],
            "longitude": response["coord"]["lon"]
            }
            return output,200'''
            
    else:
        url=f'http://api.openweathermap.org/data/2.5/weather?zip={l},IN&appid={KEY}&units=metric'
        response = requests.get(url).json()

        if response.get('cod') != 200:
            return report_error,404
        else:
            output={
            "country":response["sys"]["country"],
            "name":response["name"],
            "temp":response["main"]["temp"],
            "min_temp": response["main"]["temp_min"],
            "max_temp": response["main"]["temp_max"],
            "latitude":response["coord"]["lat"],
            "longitude": response["coord"]["lon"]
            }
            return output,200
       
           





