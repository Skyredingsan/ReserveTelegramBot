import psycopg2
from psycopg2 import Error
import telebot
from Settings import TOKEN

bot = telebot.TeleBot(TOKEN)

result = 0

def authentication(message):
    userid = message.chat.id #берем userid для сверения с бд
    print(userid) #вывод userid в консоль телеграмма (доработать: убрать это в файл с логами)

    # Подключение к БД
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

        # Проверяем есть ли данный пользователь в БД. Если нет возвращается NULL
        cursor.execute(f'SELECT first_name,second_name FROM employer WHERE telegram_id={userid}')

        #сохраняем результат для авторизации
        global result
        result = cursor.fetchall()

    # В случае ошибки с PostgreSQL и закрытие
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return result