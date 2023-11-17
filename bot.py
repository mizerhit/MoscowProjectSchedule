import telebot
from telebot import types
# import menu

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
menu_btn3 = types.KeyboardButton("Выбор группы")
menu_mark.add(menu_btn1, menu_btn2, menu_btn3)

homework_btn2 = types.KeyboardButton("Добавление дз")
homework_btn1 = types.KeyboardButton("Просмотр дз")
homework_mark.add(homework_btn1, homework_btn2)

subject_btn2 = types.KeyboardButton("Выберите предмет")
# subject_btn1 = types.KeyboardButton("Дз на неделю")
subject_mark.add(subject_btn2)


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
        bot.send_message(message.from_user.id, "Введите ДЗ: Предмет-> дз")
        bot.register_next_step_handler(message, get_homework)

    elif message.text == "Выбрать предмет":
        bot.send_message(message.from_user.id, "К какому предмету дз? ")

    elif message.text == "Выберите предмет":
        bot.send_message(message.from_user.id, "Введите название предмета")
        bot.register_next_step_handler(message, get_subject)

    elif message.text == "Просмотр дз":
        bot.send_message(message.from_user.id, "Какое дз хотите посмотреть?",
                         reply_markup=subject_mark)

    # elif message.text == "Дз на неделю":
    #     bot.send_message(message.from_user.id, homework)

    elif message.text == "Выбор группы":
        bot.send_message(message.from_user.id, "Введите название вашей группы")
        bot.register_next_step_handler(message, get_group)

    else:
        bot.send_message(message.from_user.id,
                         "Я вас не понимаю, для просмотра команд введите /help")


def get_homework(message):
    global homework
    homework = message.text
    bot.send_message(message.from_user.id, "Домашняя работа добавленна",
                     reply_markup=menu_mark)


def get_subject(message):
    global subject
    subject = message.text
    bot.send_message(message.from_user.id, "Вот ДЗ",
                     reply_markup=menu_mark)


def get_group(message):
    global group
    group = message.text
    bot.send_message(message.from_user.id, text="Группа добавлена",
                     reply_markup=menu_mark)
    bot.send_message(message.from_user.id, group)
    print(message.from_user.username)


bot.polling(none_stop=True, interval=0)
