import threading
from datetime import datetime
import time
import telebot
from dbstuff import DbQuery
from parsetable import specValue
import re


emoji_up = u'\U0001F53A'
emoji_down = u'\U0001F53B'


repattern = r'[^а-яА-Я -]'

def get_position(db, name, spec):
    spec_data = db.get_spec_list(spec)
    for i in range(len(spec_data)):
        if spec_data[i][0] == name:
            return i + 1


def get_position_upd(db, name, spec, upd):
    spec_data = db.get_spec_list_upd(spec, upd)
    for i in range(len(spec_data)):
        if spec_data[i][0] == name:
            return i + 1
    return -1


def loop_update(): #every 2 hours
    while True:
        print('updating db')
        db = DbQuery()
        c_time = int(datetime.today().timestamp())
        db.insert_all(c_time)
        del db
        print('done updating')
        time.sleep(7200)


def filter_name(s):
    s = re.sub(repattern, '', s)
    return s


def send_message_to_subscribers(): #once a day
    while True:
        db = DbQuery()
        subs = db.get_subs()
        c_time = int(datetime.today().timestamp())
        prev_upd = db.get_closest_upd(c_time - 86000)
        for sub in subs:
            c_user = db.find_user(sub[0])
            c_pos = []
            for row in c_user:
                t_pos = get_position(db, sub[0], row[9])
                c_pos.append([row[9], t_pos])
            p_pos = []
            answer = str(sub[0]) + '\n'
            for i in range(len(c_pos)):
                t_pos = get_position_upd(db, sub[0], c_pos[i][0], prev_upd)
                answer += "\"" + str(specValue[c_pos[i][0]]) + "\"" + ' место: ' + str(c_pos[i][1]) + ' '
                if t_pos > c_pos[i][1]:
                    answer += emoji_down
                elif t_pos < c_pos[i][1]:
                    answer += emoji_up
                answer += '\n'
            bot.send_message(sub[1], answer)

        time.sleep(86400)


TOKEN = '1394904859:AAG--El2aQs5XPNnZl9LvD2gQaGpsFmXik4'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    bot.reply_to(message, "Чтобы узнать свое место в списках поступающих напишите свои Фамилия Имя Отчество")


@bot.message_handler(commands=['subscribe'])
def sub_to_updates(message):
    db = DbQuery()
    name = message.text[11:]
    name = filter_name(name)
    print(name)
    result = db.find_user(name)
    if len(result) == 0:
        answer = "Такой Абитуриент не найдет"
    else:
        db.insert_sub(name, message.chat.id)
        answer = "Вы успешно подписались на рассылку! \nЕсли хотите отписаться, то просто напишите /unsubscribe"
    bot.reply_to(message, answer)


@bot.message_handler(commands=['unsubscribe'])
def unsub_from_updates(message):
    db = DbQuery()
    db.delete_sub(message.chat.id)
    bot.reply_to(message, 'Вы отписались от рассылки')


@bot.message_handler(content_types=['text'])
def get_name(message):
    db = DbQuery()
    message.text = filter_name(message.text)
    result = db.find_user(message.text)
    print(message.text)
    answer = ''

    if len(result) == 0:
        answer = "Такой Абитуриент не найдет"
    else:
        for row in result:
            answer += "\"" + str(specValue[row[9]]) + "\"" + ' место: ' + str(
                get_position(db, message.text, row[9])) + '\n'
    bot.reply_to(message, answer)
# 9 for spec


x = threading.Thread(target=loop_update)
x.start()
y = threading.Thread(target=send_message_to_subscribers)
y.start()
bot.polling()
