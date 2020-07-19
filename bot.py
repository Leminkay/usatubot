import requests
from datetime import datetime
import telebot
import dbstuff
from parsetable import specValue

def get_position(db, name, spec):
    specData = db.get_spec_list(spec)
    for i in range(len(specData)):
        if specData[i][0] == name:
            return i + 1



TOKEN = '1394904859:AAGnS2IQuE3EDOnwI69bCt6HovM-a3U5Luc'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help_message(message):
    bot.reply_to(message,"Чтобы узнать свое место в списках поступающих напишите свои Фамилия Имя Отчество")
@bot.message_handler(content_types=['text'])
def get_name(message):
    db = dbstuff.DbQuery()
    result = db.find_user(message.text)
    answer = ''
    if len(result) == 0:

        answer = "Такой Абитуриент не найдет"
    else:
        for row in result:
            answer += "\"" + str(specValue[row[9]]) + "\"" + ' место: ' + str(get_position(db, message.text, row[9])) + '\n'
    bot.reply_to(message, answer)
#9 for spec

bot.polling()