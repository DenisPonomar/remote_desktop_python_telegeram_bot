print("Запуск бота...")
import telebot
from telebot import apihelper
from telebot import types
import subprocess
import os

f = open('tg_token.txt', 'r')
tg_token = f.read()
f.close()

bot = telebot.TeleBot(tg_token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Запустить калькулятор")
    btn2 = types.KeyboardButton("Запустить Chrome")
    btn3 = types.KeyboardButton("Запустить Firefox")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, я бот для управления твоим компьютером!", reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Запустить калькулятор"):
        os.system('start calc')
    elif(message.text == "Запустить Chrome"):
        os.system("start chrome")
    elif(message.text == "Убить Chrome"):
        os.system("Taskkill /IM chrome.exe /F")
    elif(message.text == "Запустить Firefox"):
        os.system("start firefox")
    elif(message.text == "Убить Firefox"):
        os.system("Taskkill /IM firefox.exe /F")
    else:
        #os.system(message.text)
        list_files = os.popen(message.text).read().encode('cp1251').decode('cp866')
        print(list_files)
        bot.send_message(message.chat.id, text=list_files)
bot.polling(none_stop=True, interval=0)
