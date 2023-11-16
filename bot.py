import telebot
from telebot import types

token = ""
bot = telebot.TeleBot(token)

schedule = """
Физика | 10:00 | B-210
________________________________________________________________
Физика | 10:00 | B-210
________________________________________________________________
Физика | 10:00 | B-210
________________________________________________________________
Физика | 10:00 | B-210 
"""


global homework
homework = "Дз нету :)"

menu_mark = types.ReplyKeyboardMarkup(one_time_keyboard=False)
homework_mark = types.ReplyKeyboardMarkup(one_time_keyboard=True)

menu_btn1 = types.KeyboardButton("Расписание")
menu_btn2 = types.KeyboardButton("Домашняя работа")
menu_mark.add(menu_btn1, menu_btn2)

homework_btn2 = types.KeyboardButton("Добавление дз")
homework_btn1 = types.KeyboardButton("Просмотр дз")
homework_mark.add(homework_btn1, homework_btn2)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Напиши /help для доп информации", reply_markup=menu_mark)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Расписание":
        bot.send_message(message.from_user.id, schedule)
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Выберите на клавиатуре или напишите Расписание или Домашняя работа")
    elif message.text == "Домашняя работа":
        bot.send_message(message.from_user.id,
                         "Просмотр или добавление ДЗ?", reply_markup=homework_mark)
    elif message.text == "Добавление дз":
        bot.send_message(message.from_user.id, "Введите ДЗ")
        bot.register_next_step_handler(message, get_homework)
    elif message.text == "Просмотр дз":
        bot.send_message(message.from_user.id, homework,
                         reply_markup=menu_mark)
    else:
        bot.send_message(message.from_user.id,
                         "Я вас не понимаю, для просмотра команд введите /help")


def get_homework(message):
    global homework
    homework = message.text
    bot.send_message(message.from_user.id, "Домашняя работа добавленна",
                     reply_markup=menu_mark)


bot.polling(none_stop=True, interval=1)
