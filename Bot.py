import telebot
import markups as m
from Settings import TOKEN
import Meeting_room as mr
import Login as lg

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
    bot.send_message(message.chat.id, message.text)

# запросы от бота на сервера телеграма на проверку новых сообщений
bot.infinity_polling(timeout=3)

'''
def authentication(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = telebot.types.KeyboardButton('Уфа')
    mr.reserveroom(message)
'''