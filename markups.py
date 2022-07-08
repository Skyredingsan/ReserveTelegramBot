from telebot import types

start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
start_markup_btn1 = types.KeyboardButton('/start')
start_markup.add(start_markup_btn1)

mymeetingroom_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
MeetingKey = types.KeyboardButton('Занять переговорную')
MyReservations = types.KeyboardButton('Мои занятые переговорные')
mymeetingroom_markup.add(MeetingKey, MyReservations)

city_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
city1 = types.KeyboardButton(text='Уфа')
city2 = types.KeyboardButton(text='Москва')
city3 = types.KeyboardButton(text='Питер')
city_markup.add(city1, city2, city3)