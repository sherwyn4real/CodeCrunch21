import requests
import os

KEY = os.getenv('WEAT_API_KEY') #api key

report_error = {
    "status": 404,
    "message": "weather data not found"
}


 

def search_city(cname):
   # city = request.args.get('q')  # city name passed as argument

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
        return output
        #result=json.dumps(output)
        #return result
         
    # get current temperature and convert it into Celsius
    #current_temperature = response.get('main', {}).get('temp')
    #if current_temperature:
       # current_temperature_celsius = round(current_temperature - 273.15, 2)
       
 #========================================================================


def search_cord_pin(l):
    
    if(type(l) == list):
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
            return output,200
            #result=json.dumps(output)
            #return result
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
            #result=json.dumps(output)
            #return result 
           





