import requests
from datetime import datetime
import telebot

TOKEN = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help_message(message):
    bot.reply_to(message,"Чтобы узнать свое место в списках поступающих напишите свои Фамилия Имя Отчество")

bot.polling()