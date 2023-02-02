import telebot
from telebot import types
from pytube import YouTube

from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """
    This function prompts the user to submit a YouTube URL.
    """
    sent = bot.reply_to(message, start_message)
    bot.register_next_step_handler(sent, get_video_resolution)


def get_video_resolution(message):
    """
    This function, in response to sending the user's URL, returns a list of video resolutions available for download.
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
    bot.send_message(callback.message.chat.id, "If you want to download new video, snt me URL again")

    # bot.register_next_step_handler(start_message, get_video_resolution)


bot.polling(none_stop=True, interval=0)
