token = '544142715:AAEm6guIXVrV5EUvUt_QjZtB6lP1tQve8OA' # полученный у @botFather
clientAccessToken = '56b86f0087cd489f839813b0ca2fbbca' # получен на DialogFlow agent = Julia_robot
DOMAIN = 'https://www.hse.ru/' # домен сайта вышки
ARGS = '?fromdate={}&todate={}&groupoid={}&receiverType=3' # аргументы для url сайта вышки
ADDR = 'api/timetable/lessons' # адрес на сайтате вышки к расписанию
faculties = ['ИМиКН','Гум.науки','Право','Экономика','Менеджмент'] # факультеты нижегородской вышки
years = ['2014','2015','2016','2017']
weather_key = 'b1ee13e86990b96bbb9985405034a165' # ключ с сайта openweathermap.org
wethar_domain='http://api.openweathermap.org/' # домен сайта openweathermap.org
weather_args= 'data/2.5/find?q={},RU&type={}' # аргументы для url сайта openweathermap.org
NN_id= '520555'

switcher = {
    'ИМиКН': ["17ПИ","16ПИ","15ПИ","14ПИ","17ФМ","16ФМ","15ФМ","17БИ1","17БИ2","17БИ3","16БИ1","16БИ2","15БИ1","15БИ2","14БИ1","14БИ2","17ПМИ1","17ПМИ2","16ПМИ","16ПМИ2","15ПМИ","14ПМИ1"],
	'Гум.науки': ["17ФИЛ","17ФИЛ2","16ФИЛ","15ФИЛ","14ФИЛ","17ФПЛ","17ФПЛ2","16ФПЛ","15ФПЛ","14ФПЛ"],
	'Право': ["17Ю1","17Ю2","17Ю3","16Ю1","16Ю2","16Ю3","15Ю1","15Ю2","14Ю1","14Ю2"],
	'Экономика': ["17Э1","17Э2","17Э3","17Э4","16Э1","16Э2","16Э3","16Э4","15Э1","15Э2","15Э3","14Э1","14Э2","14Э3","14Э4"],
	'Менеджмент': ["17М1","17М2","17М3","17М4","16М1","16М2","16М3","16М4","15М1","15М2","15М3","15М4"]
}