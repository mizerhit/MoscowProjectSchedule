import telebot
from telebot import types

token = "6398606477:AAEIIC64vT5WqQrgoDnaaIuc6NM_694F3RA"
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

menu_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=False, resize_keyboard=True, row_width=2)
homework_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)
subject_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)

menu_btn1 = types.KeyboardButton("Расписание")
menu_btn2 = types.KeyboardButton("Домашняя работа")
menu_mark.add(menu_btn1, menu_btn2)

homework_btn2 = types.KeyboardButton("Добавление дз")
homework_btn1 = types.KeyboardButton("Просмотр дз")
homework_mark.add(homework_btn1, homework_btn2)

subject_btn2 = types.KeyboardButton("Выберите предмет")
subject_btn1 = types.KeyboardButton("Дз на неделю")
subject_mark.add(subject_btn1, subject_btn2)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Напиши /help для доп информации", reply_markup=menu_mark)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Расписание":
        bot.send_message(message.from_user.id, schedule)
        print(message.from_user.id, message.from_user.first_name,
              message.from_user.last_name, message.from_user.username)

    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Выберите на клавиатуре или напишите Расписание или Домашняя работа")

    elif message.text == "Домашняя работа":
        bot.send_message(message.from_user.id,
                         "Просмотр или добавление ДЗ?", reply_markup=homework_mark)

    elif message.text == "Добавление дз":
        bot.send_message(message.from_user.id, "Введите ДЗ: Предмет-> дз")

    elif message.text == "Выбрать предмет":
        bot.send_message(message.from_user.id, "К какому предмету дз? ")

    elif message.text == "Выберите предмет":
        bot.send_message(message.from_user.id, "Список предметов:")

    elif message.text == "Просмотр дз":
        bot.send_message(message.from_user.id, homework,
                         reply_markup=subject_mark)

    elif message.text == "Дз на неделю":
        bot.send_message(message.from_user.id, homework)

    else:
        bot.send_message(message.from_user.id,
                         "Я вас не понимаю, для просмотра команд введите /help")


def get_homework(message):
    global homework
    homework = message.text
    bot.send_message(message.from_user.id, "Домашняя работа добавленна",
                     reply_markup=menu_mark)


bot.polling(none_stop=True, interval=0)
