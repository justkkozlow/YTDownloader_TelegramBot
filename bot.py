import telebot
from telebot import types
from pytube import YouTube

from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Handler prompts the user to submit a YouTube URL.
    /////
    Обработчик предлагает пользователю отправить URL-адрес YouTube.
    """
    sent = bot.send_message(message.chat.id, sent_url)
    bot.register_next_step_handler(sent, get_video_resolution)


def get_video_resolution(message):
    """
    Handler, in response to sending the user's URL, ask what resolution quality to download video
    /////
    Обработчик, в ответ на отправку URL пользователя, спрашивает в каком разрешении скачивать видео
    """
    global youtube_link
    youtube_link = message.text
    kb = types.InlineKeyboardMarkup(row_width=3)
    low_resolution = types.InlineKeyboardButton("Low resolution", callback_data='low')
    hight_resolution = types.InlineKeyboardButton("Hight resolution", callback_data='hight')
    kb.add(low_resolution, hight_resolution)
    bot.send_message(message.chat.id, video_is_ready, reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: True)
def get_video_from_youtube(callback):
    """
    Handler for downloading video in selected resolution
    /////
    Обработчик для загрузки видео в выбранном разрешении
    """
    yt = YouTube(youtube_link)
    if callback.data == 'low':
        stream = yt.streams.get_lowest_resolution()
        stream.download("download", filename="video_low.mp4")
        file = open('download/video_low.mp4', 'rb')
    elif callback.data == 'hight':
        stream = yt.streams.get_highest_resolution()
        stream.download("download", filename="video_hight.mp4")
        file = open('download/video_hight.mp4', 'rb')
    bot.send_video(callback.message.chat.id, file)

    new_url = bot.send_message(callback.message.chat.id, ctn_url)
    bot.register_next_step_handler(new_url, get_video_resolution)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
