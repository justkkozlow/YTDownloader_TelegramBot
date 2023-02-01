import time

import telebot
from telebot import types
from pytube import YouTube

from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    This function prompts the user to submit a YouTube URL.
    :param message:
    """
    sent = bot.reply_to(message, start_message)
    bot.register_next_step_handler(sent, get_resolution_list)


def get_resolution_list(message):
    """
    This function, in response to sending the user's URL, returns a list of video resolutions available for download.
    :param message:
    """
    message_to_save = message.text
    yt = YouTube(message_to_save)
    kb = types.InlineKeyboardMarkup(row_width=3)
    resolution_list = yt.streams.filter(file_extension="mp4", type="video", progressive=True)
    for i in resolution_list:
        btn = types.InlineKeyboardButton(f'{i.resolution} {i.fps}fps', callback_data="!!!")
        kb.add(btn)
    stream = yt.streams.get_highest_resolution()
    stream.download("download", filename="video.mp4")
    bot.send_message(message.chat.id, choose_resolution_message, reply_markup=kb)  # Answer


@bot.message_handler(content_types=["video"])
def handle_files(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    print(document_id)  # Выводим file_id
    print(f'http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')  # Выводим ссылку на файл
    bot.send_message(message.chat.id, document_id)  # Отправляем пользователю file_id


@bot.callback_query_handler(func=lambda callback: True)
def send_something(callback):
    time.sleep(10)
    if callback.data == "!!!":
        file = open('download/video.mp4', 'rb')
        bot.send_message(callback.message.chat.id, "After downloading you can get your video:")
        bot.send_video(callback.message.chat.id, file)


bot.polling()
