import telebot
from telebot import types

bot = telebot.TeleBot("6589767577:AAGKFb8zb4x5gxNr0Gnn3_jVE1hyn_GYHDc")

keyboard = types.ReplyKeyboardMarkup(row_width=5)

button_list = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15"
]
for name in button_list:
    print(name)
keyboard.add(*[types.KeyboardButton(name) for name in button_list])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Choose a number:", reply_markup=keyboard)

bot.polling()