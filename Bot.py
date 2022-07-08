import telebot
from telebot import types

import Meeting_room
from Settings import TOKEN
import Meeting_room as mr
import Login as lg

bot = telebot.TeleBot(TOKEN)

#начало рабоыт с ботом
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    MeetingKey = types.KeyboardButton('Занять переговорную')
    MyReservations = types.KeyboardButton('Мои занятые переговорные')
    markup.add(MeetingKey, MyReservations)

    lg.authentication(message)
    if lg.result != []:
        for row in lg.result:
            bot.send_message(message.chat.id, f'Здравствуйте, {row[0]} {row[1]}, что вы желаете сделать?', reply_markup=markup)
    else:
        bot.send_message('Ошибка доступа')

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.text == 'Занять переговорную':
        mr.reserveroom(message)
    if message.text == 'Мои занятые переговорные':
        bot.send_message(message.chat.id, 'В разработке')

#вывод списка переговорных при нажатии на инлайн кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    mr.callback_button_room(call)

# запросы от бота на сервера телеграма на проверку новых сообщений
bot.infinity_polling(timeout=20)

'''
def authentication(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = telebot.types.KeyboardButton('Уфа')
    mr.reserveroom(message)
'''