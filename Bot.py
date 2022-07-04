import telebot
from Settings import TOKEN
import Meeting_room as mr

bot = telebot.TeleBot(TOKEN)

#начало рабоыт с ботом
@bot.message_handler(commands=['start'])
def authentication(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = telebot.types.KeyboardButton('Уфа')
    mr.reserveroom(message)

#вывод списка переговорных при нажатии на инлайн кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    mr.callback_button_room(call)

# запросы от бота на сервера телеграма на проверку новых сообщений
bot.infinity_polling(timeout=20)

