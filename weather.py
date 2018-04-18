import config
import requests
import datetime
s_city = "Nizhniy Novgorod, RU"
    
def get_weather():
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",params={'id': config.NN_id, 'units': 'metric', 'lang': 'ru', 'APPID': config.weather_key})
    data = res.json()
    list = []
    i = 0
    inf = data['list'][0] 
    day = inf['dt_txt'][8] + inf['dt_txt'][9]
    list.append([inf['dt_txt'], '{0:+3.0f}'.format(inf['main']['temp']), '{0:3.0f}м/с'.format(inf['wind']['speed']), get_wind(int(inf['wind']['deg'])),inf['weather'][0]['description']])
    for data in data['list']:
        str = data['dt_txt'][8] + data['dt_txt'][9]
        time = data['dt_txt'][11] + data['dt_txt'][12]
        if str != day and time=='12':
            wind = get_wind(int(data['wind']['deg']))
            list.append([data['dt_txt'], '{0:+3.0f}'.format(data['main']['temp']), '{0:3.0f}м/с'.format(data['wind']['speed']), wind,data['weather'][0]['description']]) 
            day = str
    l = list[0]
    return list		
	
def get_wind(deg):
    if deg>=337 or deg <=22:
	    wind = 'C'
    elif 292 <= deg <= 337:
        wind = 'CЗ'
    elif 247 <= deg <=292:
        wind = 'З'
    elif 202 <= deg <= 247:
        wind = 'ЮЗ'
    elif 157 <= deg <= 202:
        wind = 'Ю'
    elif 112 <= deg <=157:
        wind = 'ЮВ'
    elif 67 <= deg <=112:
        wind = 'В'
    else:
        wind = 'CВ'
    return wind
	
def get_weatherEmoji(description):
    switcher = {
        "легкий дождь": "\U00002614",
        "ясно": "\U00002600",
        "облачно":"\U00002601",
        "пасмурно": "\U00002601",
        "дождь":"\U00002614",
        "переменная облачность": "\U000026C5",
        "небольшой снегопад": "\U00002744"
	}
    emoji = switcher.get(description," ")
    return emoji