import telebot
import markups as m
from Settings import TOKEN
import Login as lg
import psycopg2
from psycopg2 import Error

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
        msgtextcity = bot.send_message(message.chat.id, str(text))  # вывод сообщения боту.
        bot.register_next_step_handler(msgtextcity, startreserveroom)

        # В случае ошибки с PostgreSQL и закрытие
    except(Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def startreserveroom(message):
    msgid = message.text
    if msgid.isdigit() == True:
        msgid = int(msgid)
        connection = psycopg2.connect(user='postgres', password='2Dota2ru', host='127.0.0.1', port='5432', database='ReserveBotBD')
        # Курсор для выполнения операций с БД
        cursor = connection.cursor()

        cursor.execute(f"SELECT meeting_room_id FROM Meeting_room where meeting_room_id = '{msgid}'")

        roomid = cursor.fetchall()
        text = '\n\n'.join([','.join(map(str, x)) for x in roomid])
        cursor.execute(f"SELECT * FROM reservedroom where meetingroomid = '{str(text)}'")

        roominfo = cursor.fetchall()
        textroom = '\n\n'.join([','.join(map(str, x)) for x in roominfo])
        bot.send_message(message.chat.id, textroom)


    else:
        #'Ошибка, введите число'
        msgerror = bot.send_message(message.chat.id, 'Введите id комнаты')
        bot.register_next_step_handler(msgerror, startreserveroom)

# запросы от бота на сервера телеграма на проверку новых сообщений
bot.infinity_polling(timeout=3)

'''
def authentication(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = telebot.types.KeyboardButton('Уфа')
    mr.reserveroom(message)
'''