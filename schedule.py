import config 
import datetime
from requests import Session

def get_table(group, groupid):
    # groupID -- i don't know what mean groupid on hse website. What is it?
    course = datetime.datetime.now().year - 2000 - int(group[0])*10 - int(group[1]) # считаем курс, исходя из группы
    today = datetime.date.today()	
	# берём текущую неделю, будем выводить расписание не текущую неделю, если воскресенье, то на следующую
    if (datetime.datetime.now().isoweekday() == 7):
        fromdate = (today - datetime.timedelta(days=1)).strftime("%Y.%m.%d")
        todate = (today + datetime.timedelta(days=6)).strftime("%Y.%m.%d")
    else:
        fromdate = (today - datetime.timedelta(days=today.weekday())).strftime("%Y.%m.%d")
        todate = (today + datetime.timedelta(days=5-today.weekday())).strftime("%Y.%m.%d")
    config.ARGS = config.ARGS.format(fromdate, todate, groupid)
    URL = ''.join((config.DOMAIN, config.ADDR, config.ARGS))
    session = Session()
    response = session.get(URL)
    table = response.json()   
    return table
	
def get_groupid(group):
	# matching groups and theirs id
    switcher = {
        "17ПИ": "6929",
        "16ПИ": "7290",
        "15ПИ": "6371",
        "14ПИ": "7237",
        "17ФМ": "6933",
        "16ФМ": "7249",
        "15ФМ": "7241",
        "17БИ1": "6911",
        "17БИ2": "6913",
        "17БИ3": "6912",
        "16БИ1": "6584",
        "16БИ2": "6583",
        "15БИ1": "6374",
        "15БИ2": "6370",
        "14БИ1": "6219",
        "14БИ2": "6218",
        "17ПМИ1": "6927",
        "17ПМИ2": "6928",
        "16ПМИ": "7247",
        "16ПМИ2": "7248",
        "15ПМИ": "7242",
        "14ПМИ1": "7238",
        "17Э1": "6934",
        "17Э2": "6930",
        "17Э3": "6935",
        "17Э4": "7605",
        "16Э1": "6611",
        "16Э2": "6604",
        "16Э3": "6605",
        "16Э4": "6606",
        "15Э1": "6367",
        "15Э2": "6379",
        "15Э3": "6380",
        "14Э1": "6229",
        "14Э2": "6230",
        "14Э3": "6228",
        "14Э4": "6231",
        "17Ю1": "6938",
        "17Ю2": "6939",
        "17Ю3": "7620",
        "16Ю1": "6607",
        "16Ю2": "6559",
        "16Ю3": "6608",
        "15Ю1": "6368",
        "15Ю2": "6369",
        "14Ю1": "6217",
        "14Ю2": "6232",
        "17ФИЛ": "6931",
        "17ФИЛ2": "7659",
        "16ФИЛ": "7245",
        "15ФИЛ": "6373",
        "14ФИЛ": "7239",
        "17ФПЛ": "6926",
        "17ФПЛ2": "7660",
        "16ФПЛ": "7246",
        "15ФПЛ": "6372",
        "14ФПЛ": "7240",
        "17М1": "6924",
        "17М2": "6932",
        "17М3": "6925",
        "17М4": "7606",									
        "16М1": "6581",
        "16М2": "6580",
        "16М3": "6579",
        "16М4": "6609",
        "15М1": "6376",
        "15М2": "6378",
        "15М3": "6375",
        "15М4": "6377"
	}
    id = switcher.get(group,"Invalid group")
    return id

def get_dayNumberOfWeek(day):
    switcher = {
        '/monday': 1,
    	'/tuesday': 2,
        '/wednesday': 3,
    	'/thursday': 4,
        '/friday': 5,
    	'/saturday': 6
    }
    return switcher.get(day)
	
def get_schedule(table, dayOfWeek): 
    lessons = table.get('Lessons')
    date = datetime.date.today().strftime("%Y.%m.%d")
    time_list=[]
    location_list=[]
    discipline_list=[]
    type_list=[]
    lecturer_list=[]
    auditorium_list=[]
    i = 0
    while i < len(lessons) and lessons[i]['dayOfWeek'] != int(dayOfWeek):
        i += 1 		
    if i == len(lessons):
	    return date, time_list, location_list, auditorium_list, discipline_list, type_list, lecturer_list
    date = lessons[i]['date']
    while i < len(lessons) and lessons[i]['dayOfWeek'] == dayOfWeek:
        auditorium_list.append(lessons[i]['auditorium'])
        time_list.append(lessons[i]['beginLesson'])
        location_list.append(lessons[i]['building'])
        discipline_list.append(lessons[i]['discipline'])
        type_list.append(lessons[i]['kindOfWork'])
        lecturer_list.append(lessons[i]['lecturer'])
        i += 1
    return date, time_list, location_list, auditorium_list, discipline_list, type_list, lecturer_list




	
