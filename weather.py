import requests
import json
import urllib.parse
from geopy.geocoders import Nominatim
import time

def rewrite_time(str1):
    a=str1.split("-")
    a[0],a[2]=a[2],a[0]
    b="-".join(a)
    return b

def meteo(location):
    geolocator = Nominatim(user_agent="msufilial14@gmail.com")
    location = geolocator.geocode(location)

    if location!=None:
        lt=str(location.latitude)
        lg=str(location.longitude)
       
        conv=float("0.750062")
        api_="2966850be97168be61066bf35e6ad295"
        #url="https://api.openweathermap.org/data/2.5/weather?lat="+lt+"&lon="+lg+"&appid=2966850be97168be61066bf35e6ad295&lang=ru&units=metric"
        url="https://api.openweathermap.org/data/2.5/forecast?lat="+lt+"&lon="+lg+"&appid=2966850be97168be61066bf35e6ad295&lang=ru&units=metric"
        response = requests.get(url)
        data = json.loads(response.text)
        a=""
        k=0
        str_=str(location)+"\n\n"

        for i in data['list']:
            if k==0:
                a=i['dt_txt'][:-8]
          
            if i['dt_txt'][:-8]!=a:
                str_=str_+"\n"

            str_=str_+rewrite_time(i['dt_txt'][:-3].split()[0])+" "+i['dt_txt'][:-3].split()[1]+" "
            str_=str_+i['weather'][0]['description']+" "+'{0:+3.0f}'.format(i['main']['temp'])+"°"+" "+str(i['wind']['speed'])+" м/c "
            str_=str_+'{0:+3.0f}'.format(i['main']['pressure']*conv)+" мм рт.ст."+"\n"
            a=i['dt_txt'][:-8]
            k=k+1

        return str_
    else:
        str_="Попробуйте изменить запрос"
        


str1="Автодорожный институт Ташкент"
r=meteo(str1)
print(r)


