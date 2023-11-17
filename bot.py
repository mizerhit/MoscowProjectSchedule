import telebot
from telebot import types
import menu as mn
import models as md
import re
# import menu

token = ""
bot = telebot.TeleBot(token)

global menu

menu_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=False, resize_keyboard=True, row_width=2)
homework_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)
subject_mark = types.ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True, row_width=2)

menu_btn1 = types.KeyboardButton("Расписание")
menu_btn2 = types.KeyboardButton("Домашняя работа")
menu_btn3 = types.KeyboardButton("Смена группы")
menu_btn4 = types.KeyboardButton("Изменение расписания")
menu_mark.add(menu_btn1, menu_btn2, menu_btn3, menu_btn4)

homework_btn2 = types.KeyboardButton("Добавление дз")
homework_btn1 = types.KeyboardButton("Просмотр дз")
homework_mark.add(homework_btn1, homework_btn2)

subject_btn2 = types.KeyboardButton("Выберите предмет")
# subject_btn1 = types.KeyboardButton("Дз на неделю")
subject_mark.add(subject_btn2)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    msg = bot.send_message(message.from_user.id,
                           "Привет! Я чат-бот, который поможет тебе не запутаться в твоём расписании и домашней работе. "
                           "Для начала пройди регистрацию: напиши свою группу АААа-11-1 (  Например, 'ИСИб-22-1')")
    bot.register_next_step_handler(msg, group)


def group(message):
    chat_id = message.chat.id
    name_group = message.text
    group_pattern = r'^[А-Яа-яЁёA-Za-z]{2,4}[бам]-\d{2}-\d+'
    if re.match(group_pattern, name_group):
        bot.send_message(chat_id, 'Вы записались в группу ' +
                         name_group + '!', reply_markup=menu_mark)
        global menu
        menu = mn.Menu(group_name=name_group)
        menu.add_student(nickname=chat_id)
        schedule = "Пусто"

        # bot.register_next_step_handler(chat_id, status)
    else:
        msg = bot.send_message(
            chat_id, 'Укажите название группы в требуемом формате')
        bot.register_next_step_handler(msg, group)

# def status(chat_id):
#     check_status = types.ReplyKeyboardMarkup()
#     yes = types.KeyboardButton('Да')
#     no = types.KeyboardButton('Нет')
#     check_status.add(yes, no)
#     bot.send_message(chat_id, 'Вы староста?', reply_markup=check_status)

# @bot.message_handler(func=lambda message: message.text=="Да")
# def group_captain(massage):
#     #добавить в бд "Captain"
# @bot.message_handler(func=lambda message: message.text == "Да")
# def group_captain(massage):
#     #добавить в бд "Student"


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Расписание":
        bot.send_message(message.from_user.id, menu.show_schedule())

    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Выберите на клавиатуре или напишите Расписание или Домашняя работа")

    elif message.text == "Домашняя работа":
        bot.send_message(message.from_user.id,
                         "Просмотр или добавление ДЗ?", reply_markup=homework_mark)

    elif message.text == "Добавление дз":
        bot.send_message(message.from_user.id, """Введите ДЗ: Предмет: Дата;
                         Само задание""", reply_markup=menu_mark)
        bot.register_next_step_handler(message, get_homework)

    elif message.text == "Изменение расписания":
        bot.send_message(message.from_user.id, """Введите расписание в формате:
                            понедельник:
                            Математика, 100, 14.00;
                            Английский язык, 200, 15.00;
                            Теория вероянтостей, 300, 16.00;""")
        bot.register_next_step_handler(message, get_schedule)

    elif message.text == "Просмотр дз":
        bot.send_message(message.from_user.id, menu.show_homework(),
                         reply_markup=menu_mark)

    elif message.text == "Смена группы":
        bot.send_message(
            message.from_user.id, "Напишите /start")
        bot.register_next_step_handler(message, get_group)

    else:
        bot.send_message(message.from_user.id,
                         "Я вас не понимаю, для просмотра команд введите /help")


def get_homework(message):
    homework = message.text
    menu.add_homework(homework)
    print(menu.show_homework())
    bot.send_message(message.from_user.id, "Домашняя работа добавленна",
                     reply_markup=menu_mark)


def get_schedule(message):
    schedule = message.text
    sch = menu.add_schedule(schedule)
    menu.format_schedule(sch)
    bot.send_message(message.from_user.id, "Расписание измененно",
                     reply_markup=menu_mark)


def get_subject(message):
    global subject
    subject = message.text
    bot.send_message(message.from_user.id, "Вот ДЗ",
                     reply_markup=menu_mark)


def get_group(message):
    group = message.text
    menu = mn.Menu(group_name=group)
    bot.send_message(message.from_user.id, text="Группа добавлена",
                     reply_markup=menu_mark)
    bot.send_message(message.from_user.id, group)
    menu.add_student(nickname=message.from_user.username)
    print(message.from_user.username)


bot.polling(none_stop=True, interval=0)
