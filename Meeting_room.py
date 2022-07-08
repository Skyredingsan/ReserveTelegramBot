import psycopg2
from psycopg2 import Error
import telebot
from Settings import TOKEN
import Login as lg

bot = telebot.TeleBot(TOKEN)


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

def ReserveSelectRoom(message):
    bot.send_message(f'Хорошо, {message}')