import telebot
import markups as m
from Settings import TOKEN
import Login as lg
import psycopg2
from psycopg2 import Error
import time
import re

bot = telebot.TeleBot(TOKEN)

#начало рабоыт с ботом
@bot.message_handler(commands=['start'])
def start_handler(message):
        lg.authentication(message)
        if lg.result != []:
            for row in lg.result:
                msg = bot.send_message(message.chat.id, f'Здравствуйте, {row[0]} {row[1]}, что вы желаете сделать?', reply_markup=m.mymeetingroom_markup)
                bot.register_next_step_handler(msg, bot_message)
        else:
            bot.send_message('Ошибка доступа')

def bot_message(message):
    if message.text == 'Занять переговорную':
        for row in lg.result:
            city_msg = bot.send_message(message.chat.id,f'Здравствуйте, {row[0]} {row[1]}, у нас имеются переговорные в 3 городах: Уфа, Питер, Москва. Выберите город', reply_markup=m.city_markup)
            bot.register_next_step_handler(city_msg, reserveroomcity)
    if message.text == 'Мои занятые переговорные':
        bot.send_message(message.chat.id, 'В разработке')

def reserveroomcity(message):
    try:
        connection = psycopg2.connect(user='postgres',password='2Dota2ru',host='127.0.0.1',port='5432',database='ReserveBotBD')
        # Курсор для выполнения операций с БД
        cursor = connection.cursor()

        # Выводим все доступные варианты переговорных в данном городе. Визуал будет изменен в дальнейшем.
        # cursor.execute(f'SELECT city,adress,room_number FROM meeting_room WHERE city={call.data}')
        cursor.execute(f"SELECT * FROM Meeting_room where city = '{message.text}'")

        room = cursor.fetchall()
        print(room)
        # Т.к. телеграм боту нужна строка, то в данной функции мы проходим по кортежку и переводим данные в строку для вывода боту
        text = '\n\n'.join([','.join(map(str, x)) for x in room])
        text = text + '\n\n Введите интересующую дату в формате Yyyy-mm-dd'
        msgtextcity = bot.send_message(message.chat.id, str(text))  # вывод сообщения боту.
        bot.register_next_step_handler(msgtextcity, selectdate)

        # В случае ошибки с PostgreSQL и закрытие
    except(Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def selectdate(message):
    global date
    date = message.text
    try:
        valid_date = time.strptime(date, '%Y-%m-%d')
        msg = bot.send_message(message.chat.id,'Введите интересующую переговорную')
        bot.register_next_step_handler(msg, startreserveroom)
    except ValueError:
        msgerror = bot.send_message(message.chat.id, 'Введите дату!')
        bot.register_next_step_handler(msgerror, selectdate)


def startreserveroom(message):
    global roomnumber
    msgid = message.text
    roomnumber = msgid
    if msgid.isdigit() == True:
        msgid = int(msgid)
        connection = psycopg2.connect(user='postgres', password='2Dota2ru', host='127.0.0.1', port='5432', database='ReserveBotBD')
        # Курсор для выполнения операций с БД
        cursor = connection.cursor()

        cursor.execute(f"SELECT meeting_room_id FROM Meeting_room where meeting_room_id = '{msgid}'")

        roomid = cursor.fetchall()
        text = '\n\n'.join([','.join(map(str, x)) for x in roomid])
        cursor.execute(f"SELECT * FROM reservedroom where meetingroomid = '{str(text)}' AND meetingday = '{date}'")

        roominfo = cursor.fetchall()

        if roominfo != []:
            textroom = '\n\n'.join([','.join(map(str, x)) for x in roominfo])
            bot.send_message(message.chat.id, textroom)
        else:
            freeroom = 'Все время в переговорной свободно, выберите начало времени бронирования'
            msg = bot.send_message(message.chat.id, freeroom)
            bot.register_next_step_handler(msg, selectstarttime)
    else:
        #'Ошибка, введите число'
        msgerror = bot.send_message(message.chat.id, 'Введите id комнаты')
        bot.register_next_step_handler(msgerror, startreserveroom)

def selectstarttime(message):
    global date_start
    msgtext = message.text
    date_start = msgtext
    match = re.fullmatch(r'\d\d:\d\d', rf'{msgtext}')
    if match:
        msg = bot.send_message(message.chat.id, 'Введите время окончания бронирования')
        bot.register_next_step_handler(msg, selectlasttime)
    else:
        msg = bot.send_message(message.chat.id, 'Введите время')
        bot.register_next_step_handler(msg, selectstarttime)

def selectlasttime(message):
    global date_end
    msgtext = message.text
    date_end = msgtext
    match = re.fullmatch(r'\d\d:\d\d', rf'{msgtext}')
    if match:
        msg = bot.send_message(message.chat.id, 'Точно забронировать на это время?')
        bot.register_next_step_handler(msg, createdbdata)
    else:
        msg = bot.send_message(message.chat.id, 'Введите время')
        bot.register_next_step_handler(msg, selectstarttime)

def createdbdata(message):
    userid = message.chat.id
    if message.text == 'Да':
        connection = psycopg2.connect(user='postgres', password='2Dota2ru', host='127.0.0.1', port='5432',
                                      database='ReserveBotBD')
        # Курсор для выполнения операций с БД
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO reservedroom VALUES ({userid},{roomnumber}, '{date}', '{date_start}', '{date_end}') ")
        cursor.execute(f"SELECT * FROM reservedroom WHERE telegramidemployer = {userid} and meetingroomid = {roomnumber} and meetingday = '{date}' and timestart = '{date_start}' and timeend = '{date_end}'")
        result = cursor.fetchall()

        if result != []:
            bot.send_message(message.chat.id, f'Бронирование прошло успешно на {date} {date_start} - {date_end}')
        else:
            bot.send_message('Произошла ошибка, попробуйте еще раз')

# запросы от бота на сервера телеграма на проверку новых сообщений
bot.infinity_polling(timeout=3)

'''
def authentication(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = telebot.types.KeyboardButton('Уфа')
    mr.reserveroom(message)
'''