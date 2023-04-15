print("Импорт библиотек...")

import telebot
from telebot import apihelper
from telebot import types
import keyboard
from pynput.keyboard import Controller, KeyCode
import pyautogui
import os
import speech_recognition as sr
import torch
import cv2
import time
import json
import requests
import platform
from PIL import Image
import logging
import sys
import datetime

print(datetime.datetime.now().strftime("%H:%M:%S"), "Запуск бота...")

f = open('tg_id.txt', 'r')
tg_id = int(f.read())
f.close()

f = open('tg_token.txt', 'r')
tg_token = f.read()
f.close()

bot = telebot.TeleBot(tg_token);

language='ru_RU'
r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Распознавание речи...')
            print(text)
            return text
        except:
            print('Извините... Повторите попытку...')
            return "Текст неразпознан"
Stream = True
def comand(text, message):
    print(text)
    if message.from_user.id == tg_id:
        if text == '⬆':
            keyboard.send('up')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == '❌':
            keyboard.send('alt+f4')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == '⬅':
            keyboard.send('left')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == '⬇':
            keyboard.send('down')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == '➡':
            keyboard.send('right')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == 'Win':
            keyboard.send('windows')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == 'Enter':
            keyboard.send('enter')
            bot.delete_message(message.chat.id, message.message_id)
        elif text == 'Другое':
            bot.send_message(message.chat.id, text="Для произвольного ввода используются 3 метода:\n├send('alt+f4')\n├send('м','и','р')\n└write('Привет!\\nЭто перенос строки')")
        elif text[:4] == 'send':
            try:
                eval("keyboard."+text)
            except Exception:
                42
        elif text[:5] == 'write':
            try:
                eval("keyboard."+text)
            except Exception:
                42
        elif text[:3] == 'код':
            try:
                eval(text[4:])
            except Exception as e:
                bot.send_message(message.chat.id, text=e)
        elif text.lower()[:9] == 'загрузить':
            try:
                doc=open(text.lower()[10:], 'rb')
                bot.send_document(message.chat.id, doc)
                doc.close()
            except Exception as e:
                bot.send_message(message.chat.id, text=e)
        else:
            try:
                list_files = os.popen(text).read().encode('cp1251').decode('cp866')
                print(list_files)
                bot.send_message(message.chat.id, text=list_files)
            except Exception:
                try:
                    print("Синтез речи")
                    
                    device = torch.device('cpu')
                    torch.set_num_threads(4)
                    local_file = 'model.pt'

                    if not os.path.isfile(local_file):
                        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                                       local_file)  

                    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
                    model.to(device)

                    example_text = text
                    sample_rate = 48000
                    speaker='baya'

                    audio_paths = model.save_wav(text=example_text,
                                                 speaker=speaker,
                                                 sample_rate=sample_rate)
                    audio = open(r'test.wav', 'rb')
                    bot.send_voice(message.chat.id, audio)
                    audio.close()
                except Exception:
                    42
    else:
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = 'model.pt'

        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                                       local_file)  

        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)

        example_text = "Ахаха, проваливай"
        sample_rate = 48000
        speaker='baya'

        audio_paths = model.save_wav(text=example_text,
                                        speaker=speaker,
                                        sample_rate=sample_rate)
        audio = open(r'test.wav', 'rb')
        try:
            bot.send_voice(message.chat.id, audio)
        except Exception:
            bot.send_voice(message.from_user.id, audio)
        audio.close()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn0 = types.KeyboardButton("💻О системе")
    btn1 = types.KeyboardButton("🌐IP-адрес")
    btn2 = types.KeyboardButton("🏁Запустить приложение")
    btn3 = types.KeyboardButton("🔫Убить приложение")
    btn4 = types.KeyboardButton("🖥Скриншот")
    btn5 = types.KeyboardButton("📷Камера")
    btn6 = types.KeyboardButton("🛑Выключение")
    btn7 = types.KeyboardButton("🔉Медиа/громкость")
    btn8 = types.KeyboardButton("⌨Клавиатура")
    btn9 = types.KeyboardButton("📤📥Файлы")
    btn10 = types.KeyboardButton("👨‍💻Ввод команды")
    markup.add(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    bot.send_message(message.chat.id, text="Привет, я бот для управления твоим компьютером!", reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = "voice"
    file_name_full="voice/"+filename+".ogg"
    file_name_full_converted="ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg.exe -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

    comand(text, message)

@bot.message_handler(content_types=['document'])
def document_processing(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as e:
        bot.send_message(message.chat.id, text=e)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "💻О системе"):
        text = ("Разрядность системы: "+platform.architecture()[0]+"\n"+
            "Связь системы: "+platform.architecture()[1]+"\n"+
            "Тип машины: "+platform.machine()+"\n"+
            "Cетевое имя компьютера: "+platform.node()+"\n"+
            "Имя платформы: "+platform.platform()+"\n"+
            "Процессор: "+platform.processor()+"\n"+
            "Версия системы: "+platform.release()+"\n"+
            "Имя системы: "+platform.system()+"\n"+
            "Версия выпуска система: "+platform.version()+"\n"+
            "Номер версии: "+platform.win32_ver()[1]+"\n"+
            "Пакет обновлений: "+platform.win32_ver()[2]+"\n"+
            "Тип ОС: "+platform.win32_ver()[2]+"\n"+
            "Редакция ОС: "+platform.win32_edition())
        bot.send_message(message.chat.id, text=text)
    elif(message.text == "🌐IP-адрес"):
        response = requests.get('http://ip-api.com/json/?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query')
        d = json.loads(response.text)
        t=" "
        for key in d:
            t = t+str(key)+": "+str(d[key])+"\n"
        bot.send_message(message.chat.id, text=t)
    elif(message.text == "🏁Запустить приложение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Запустить Firefox', callback_data="start Firefox"))
        markup.add(telebot.types.InlineKeyboardButton(text='Запустить Фотошоп', callback_data="C:\Program Files\Adobe\Adobe Photoshop 2022\Photoshop.exe"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "🔫Убить приложение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Убить Firefox', callback_data="taskkill /IM firefox.exe /F"))
        markup.add(telebot.types.InlineKeyboardButton(text='Убить Фотошоп', callback_data="taskkill /IM Photoshop.exe /F"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "🖥Скриншот"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Скриншот', callback_data="Скриншот"))
        markup.add(telebot.types.InlineKeyboardButton(text='Стрим', callback_data="Стрим"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "📷Камера"):
            markup = telebot.types.InlineKeyboardMarkup()
            x = 0
            for i in range(10):
                cam = cv2.VideoCapture(i)
                result, image = cam.read()
                if result:
                    markup.add(telebot.types.InlineKeyboardButton(text=("Камера "+str(i)), callback_data=("Камера "+str(i))))
                    x = x + 1
            if x == 0:
                bot.send_message(message.chat.id, text="Камеры не найдены")
            else:
                bot.send_message(message.chat.id, text="Список камер", reply_markup=markup)
    elif(message.text == "🛑Выключение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выключить', callback_data="shutdown /s /t 0"))
        markup.add(telebot.types.InlineKeyboardButton(text='Перезагрузить', callback_data="shutdown /r /t 0"))
        markup.add(telebot.types.InlineKeyboardButton(text='Заблокировать', callback_data="Rundll32.exe user32.dll,LockWorkStation"))
        markup.add(telebot.types.InlineKeyboardButton(text='Разблокировать', callback_data="Разблокировать"))
        markup.add(telebot.types.InlineKeyboardButton(text='Выйти', callback_data="shutdown /l"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "🔉Медиа/громкость"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='⏮', callback_data="⏮"))
        markup.add(telebot.types.InlineKeyboardButton(text='⏹', callback_data="⏹"))
        markup.add(telebot.types.InlineKeyboardButton(text='⏯', callback_data="⏯"))
        markup.add(telebot.types.InlineKeyboardButton(text='⏭', callback_data="⏭"))
        markup.add(telebot.types.InlineKeyboardButton(text='🔈', callback_data="🔈"))
        markup.add(telebot.types.InlineKeyboardButton(text='🔊', callback_data="🔊"))
        markup.add(telebot.types.InlineKeyboardButton(text='🔇', callback_data="🔇"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "⌨Клавиатура"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn0 = types.KeyboardButton("/start")
        btn1 = types.KeyboardButton("⬆")
        btn2 = types.KeyboardButton("❌")
        btn3 = types.KeyboardButton("⬅")
        btn4 = types.KeyboardButton("⬇")
        btn5 = types.KeyboardButton("➡")
        btn6 = types.KeyboardButton("Win")
        btn7 = types.KeyboardButton("Enter")
        btn8 = types.KeyboardButton("Другое")
        markup.add(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        bot.send_message(message.chat.id, text="Кнопки клавиатуры", reply_markup=markup)
    elif(message.text == "📤📥Файлы"):
        bot.send_message(message.chat.id, text="Формат команды для скачивания файлов:\nЗагрузить C:\\1.txt\nДля закачивания файла просто отправье его как документ, он будет находиться в папке с программой.\nЛимиты Telegram:\n├📥Отправка файла боту20 МБ\n└📤Отправка ботом файла 50 МБ\n")
    elif(message.text == "👨‍💻Ввод команды"):
        bot.send_message(message.chat.id, text="Формат выполнения произвольного кода на удалённой машине:\n└код print('Hello World')")
    else:
        comand(message.text, message)
@bot.callback_query_handler(func=lambda call: True)
def _worker(call):
    global Stream
    if call.data[:6].lower() == 'камера':
        print(4)
        if -1 < int(call.data[7]) < 10:
            print(8)
            cam = cv2.VideoCapture(int(call.data[7]))
            result, image = cam.read()
            if result:
                cv2.imwrite("camera.png", image)
                photo=open('camera.png', 'rb')
                bot.send_document(call.from_user.id, photo)
                photo.close()
                os.remove('camera.png')
            else:
                bot.send_message(call.from_user.id, text="Камера не найдена!:")
    elif call.data == '⏮':
        Controller().press(KeyCode.from_vk(0xB1))
    elif call.data == '⏹':
        Controller().press(KeyCode.from_vk(0xB2))
    elif call.data == '⏯':
        Controller().press(KeyCode.from_vk(0xB3))
    elif call.data == '⏭':
        Controller().press(KeyCode.from_vk(0xB0))
    elif call.data == '🔈':
        Controller().press(KeyCode.from_vk(0xAE ))
    elif call.data == '🔊':
        Controller().press(KeyCode.from_vk(0xAF))
    elif call.data == '🔇':
        Controller().press(KeyCode.from_vk(0xAD))
    elif call.data == 'Закрыть стрим':
        Stream = False
        bot.send_message(call.from_user.id, text="Стрим закрыт")
    elif call.data.lower() == 'скриншот':
            screen = pyautogui.screenshot('screenshot.png')
            photo=open('screenshot.png', 'rb')
            bot.send_document(call.from_user.id, photo)
            photo.close()
            os.remove('screenshot.png')
    elif call.data.lower() == 'стрим':
            i = 1
            while True:
                if Stream == False:
                    Stream = True
                    break
                screen = pyautogui.screenshot()
                photo = screen.resize((640,360),Image.Resampling.LANCZOS)
                bot.delete_message(call.from_user.id, call.message.message_id+i-1)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Закрыть стрим', callback_data="Закрыть стрим"))
                bot.send_photo(call.from_user.id, photo, reply_markup=markup)
                photo.close()
                i = i + 1
                time.sleep(5)
    else:
        comand(call.data, call)

while True:
    try:
        sys.stdout.write(("\r"+datetime.datetime.now().strftime("%H:%M:%S")+" Установка соединения...     \n"))
        time.sleep(1)
        #sys.stdout.flush()
        bot.polling()
    except Exception:
        sys.stdout.write(("\r"+datetime.datetime.now().strftime("%H:%M:%S")+" Не получается соединиться...   "))
        sys.stdout.flush()
        sys.stdout.flush()
        time.sleep(1)
