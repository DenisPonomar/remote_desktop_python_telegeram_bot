import telebot
from telebot import apihelper
from telebot import types
import keyboard
import pyautogui
import uuid
import os
import speech_recognition as sr
import torch

f = open('tg_id.txt', 'r')
tg_id = int(f.read())
f.close()

f = open('tg_token.txt', 'r')
tg_token = f.read()
f.close()

bot = telebot.TeleBot(tg_token);
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

def comand(text, message):
    if text == 'заблокировать':
        cmd = "Rundll32.exe user32.dll,LockWorkStation"
    elif text == 'калькулятор':
        cmd = "calc"
    elif text == 'блокнот':
        cmd = "notepad"
    elif text == 'закрыть':
        keyboard.press_and_release('alt+f4')
    elif text == 'Интер':
        keyboard.press_and_release('enter')
    elif text == 'скрин':
        screen = pyautogui.screenshot('screenshot.png')
        photo=open('screenshot.png', 'rb')
        bot.send_document(message.chat.id, photo)
        photo.close()
        os.remove('screenshot.png')
    else:
        keyboard.write(text+" ")

    if "cmd" in locals():
        list_files = os.popen(cmd).read().encode('cp1251').decode('cp866')
        print(list_files)
        try:
            bot.send_message(call.message.chat.id, text=list_files)
        except Exception:
            42
    

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Запустить приложение")
    btn2 = types.KeyboardButton("Убить приложение")
    btn3 = types.KeyboardButton("Выключение")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, я бот для управления твоим компьютером!", reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
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
    
    try:
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



@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Запустить приложение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Запустить Firefox', callback_data="start Firefox"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "Убить приложение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Убить Firefox', callback_data="taskkill /IM firefox.exe /F"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    elif(message.text == "Выключение"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выключить', callback_data="shutdown /s /t 0"))
        markup.add(telebot.types.InlineKeyboardButton(text='Перезагрузить', callback_data="shutdown /r /t 0"))
        markup.add(telebot.types.InlineKeyboardButton(text='Заблокировать', callback_data="заблокировать"))
        markup.add(telebot.types.InlineKeyboardButton(text='Выйти', callback_data="shutdown /l"))
        bot.send_message(message.chat.id, text="Какое действие выполнить:", reply_markup=markup)
    else:
        #os.system(message.text)
        list_files = os.popen(message.text).read().encode('cp1251').decode('cp866')
        print(list_files)
        bot.send_message(message.chat.id, text=list_files)

@bot.callback_query_handler(func=lambda call: True)
def _worker(call):
    comand(call.data, call)

bot.polling()
