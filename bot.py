import requests
from datetime import datetime
import telebot
import dbstuff
from parsetable import specValue


TOKEN = '1394904859:AAGnS2IQuE3EDOnwI69bCt6HovM-a3U5Luc'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help_message(message):
    bot.reply_to(message,"Чтобы узнать свое место в списках поступающих напишите свои Фамилия Имя Отчество")
@bot.message_handler(content_types=['text'])
def get_name(message):
    db = dbstuff.DbQuery()
    res = db.find_user(message.text)
    if len(res) == 0:
        bot.reply_to(message, "Такой Абитуриент не найдет")
    else:
        for us in res:
            bot.reply_to(message, specValue[us[9]])
            print(us)


bot.polling()