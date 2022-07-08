import psycopg2
from psycopg2 import Error
import telebot
from Settings import TOKEN
import Login as lg

bot = telebot.TeleBot(TOKEN)

#функция вывода списка переговорных.
def reserveroom(message):
    global login
    userid = message.chat.id
    lg.authentication(message) #авторизация
    markup = telebot.types.InlineKeyboardMarkup() #инлайн кнопки
    if lg.result != []:
        for row in lg.result:
            city1 = telebot.types.InlineKeyboardButton(text='Уфа', callback_data='Уфа')
            city2 = telebot.types.InlineKeyboardButton(text='Москва', callback_data='Москва')
            city3 = telebot.types.InlineKeyboardButton(text='Питер', callback_data='Питер')
            markup.add(city1, city2, city3)
            bot.send_message(userid, f'Здравствуйте, {row[0]} {row[1]}, у нас имеются переговорные в 3 городах: Уфа, Питер, Москва. Выберите город', reply_markup=markup)

    else:
        bot.reply_to(message, 'Доступ запрещен, обратитесь к уполномоченному администратору')

#Ответ на нажатие inline кнопки.
def callback_button_room(call):
        try:
            connection = psycopg2.connect(
                user='postgres',
                password='2Dota2ru',
                host='127.0.0.1',
                port='5432',
                database='ReserveBotBD'
            )

            # Курсор для выполнения операций с БД
            cursor = connection.cursor()

            # Выводим все доступные варианты переговорных в данном городе. Визуал будет изменен в дальнейшем.
            #cursor.execute(f'SELECT city,adress,room_number FROM meeting_room WHERE city={call.data}')
            cursor.execute(f"SELECT * FROM Meeting_room where city = '{call.data}'")

            room = cursor.fetchall()
            print(room)
            #Т.к. телеграм боту нужна строка, то в данной функции мы проходим по кортежку и переводим данные в строку для вывода боту
            text = '\n\n'.join([','.join(map(str,x)) for x in room])
            if lg.result != []:
                bot.send_message(call.message.chat.id, str(text)) #вывод сообщения боту.
            else:
                bot.send_message(call.message.chat.id, "Ошибка доступа")

        # В случае ошибки с PostgreSQL и закрытие
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

def reserve_room_id(message):
    a=1