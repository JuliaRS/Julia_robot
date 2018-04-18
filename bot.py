import config
import schedule
import weather
import telepot # framework
import telebot # library
from telebot import types
import datetime
import apiai, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


JBot = telebot.TeleBot(config.token) # Julia Bot

# start
@JBot.message_handler(commands=['start','description'])
def start(message):
    JBot.send_message(message.chat.id,text = "Привет студент НИУ ВШЭ НН!\U0001F393 \nЯ Julia helper\U0001F60A\nЧтобы узнать чем я могу тебе помочь набери \"\help\"\nДавай немного отвлечемся от учёбы и пообщаемся?\U0001F47B")

# help
@JBot.message_handler(commands=['help'])	
def help(message):
    JBot.send_message(message.chat.id,"Я умею:\n\U00002714/today\n\U00002714/tomorrow\n\U00002714/monday(/tuesday, /wednesday, /thursday, /friday, /saturday) - расписание\n\U00002714/site\n\U00002714/weather\nА вообще давай лучше поболтаем?\U0001F60B")
	
# текущая дата и время и погода
@JBot.message_handler(commands=['today'])
def handle_today(message):
    list = weather.get_weather();
    l = list[0]
    response = ''
    emoji = weather.get_weatherEmoji(l[4])
    response += '\U0001F4C5<b>{}</b> {} {},{}\n{}{}\n'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),l[1],l[2],l[3],emoji,l[4])
    JBot.send_message(message.chat.id, response, parse_mode='HTML')
	
# дата и погода на завтра
@JBot.message_handler(commands=['tomorrow'])
def handle_today(message):
    list = weather.get_weather();
    l = list[1]
    response = ''
    emoji = weather.get_weatherEmoji(l[4])
    date = ""
    for i in range(10):
        date += l[0][i]
    response += '\U0001F4C5<b>{}</b> {} {},{}\n{}{}\n'.format(date,l[1],l[2],l[3],emoji,l[4])
    JBot.send_message(message.chat.id, response,parse_mode='HTML')	
	
# погода на текущий момент и 4 дня вперёд
@JBot.message_handler(commands=['weather'])
def handle_today(message):
    list = weather.get_weather();
    response = '' 
    for l in list:
        emoji = weather.get_weatherEmoji(l[4])
        date = ""
        for i in range(10):
            date += l[0][i]
        response += '\U0001F4C5<b>{}</b> {} {},{}\n{}{}\n\n'.format(date,l[1],l[2],l[3],emoji,l[4])
    JBot.send_message(message.chat.id, response, parse_mode='HTML')		

# расписание на любой из дней недели
@JBot.message_handler(commands=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])
def handle_schedule(message):
    if (message.text == '/sunday'):
        response = '\U0001F4C5<b>нет пар</b>'
        JBot.send_message(message.chat.id,response,parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(faculty) for faculty in config.faculties])
        faculty = JBot.send_message(message.chat.id,'Какой факультет?',reply_markup = keyboard)
        global day
        day = message.text
        JBot.register_next_step_handler(faculty, get_year)
def get_year(faculty):  
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(y) for y in config.years])
    global list
    list = config.switcher.get(faculty.text)
    year = JBot.send_message(faculty.chat.id,'Какой год поступления?',reply_markup = keyboard)
    JBot.register_next_step_handler(year, get_group)
def get_group(year):
    group_list = []
    y = int(year.text[2])*10 + int(year.text[3])
    for group in list:
        cur_year = int(group[0])*10 + int(group[1])
        if (cur_year == y):
            group_list.append(group)
    if (len(group_list) == 0):
        response = '<b>нет такой группы</b>'
        JBot.send_message(year.chat.id,response,parse_mode='HTML',reply_markup=types.ReplyKeyboardRemove())
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(gr) for gr in group_list])
        group = JBot.send_message(year.chat.id,'Какая группа?',reply_markup = keyboard)
        JBot.register_next_step_handler(group, get_schedule)        
def get_schedule(group):	
    dayOfWeek = schedule.get_dayNumberOfWeek(day)
    groupId = schedule.get_groupid(group.text)
    response = ''
    if groupId == str("Invalid group"):
        response += '<b>нет такой группы</b>'
    else:		
        date, time_lst, location_lst, auditorium_lst, discipline_lst, type_lst, lecturer_lst = schedule.get_schedule(schedule.get_table(group.text, groupId),dayOfWeek)
        response +='\U0001F4C5<b>{}</b>\n'.format(date)
        for time, location, auditorium, discipline, type, lecturer in zip(time_lst, location_lst, auditorium_lst, discipline_lst, type_lst, lecturer_lst):
           response += '\U0000270F<b>{}</b> {}, ayд.{}\n<b>{}</b>: {}, {}\n'.format(time, location, auditorium, type, discipline, lecturer)
        if len(location_lst) == 0:
            response += '<b>нет пар</b>'
    JBot.send_message(group.chat.id,response,parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

#перейти на сайт ВШЭ
@JBot.message_handler(commands = ['site'])
def handle_site(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_to_hse_site= types.InlineKeyboardButton(text='НИУ ВШЭ НН', url='https://nnov.hse.ru/')
    keyboard.add(btn_to_hse_site)
    JBot.send_message(message.chat.id, "Нажми на кнопку для перехода на сайт", reply_markup = keyboard)	

@JBot.message_handler(content_types=['text'])
def repeat_all_messages(message): 
    request = apiai.ApiAI(config.clientAccessToken).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # язык запроса
    request.session_id = 'BlaBlaBot' # ID Сессии диалога (понадобится при обучении бота)
    request.query = message.text # посылаем сообщение пользователя на DialogFlow
    respJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = respJson['result']['fulfillment']['speech'] # парсим JSON и получаем ответ
    # Если ответа нет, то значит бот его не понял
    if response:
        JBot.send_message(message.chat.id, text=response)
    else:
        JBot.send_message(message.chat.id, text='Ой, ой! Что-то совсем не понятно ')

if __name__ == '__main__':
    JBot.polling(none_stop=True)