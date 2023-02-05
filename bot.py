import telebot
from telebot import types
from pytube import YouTube
from pytube.exceptions import RegexMatchError

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
    bot.register_next_step_handler(sent, check_url)

def check_url(message):
    """
    The handler checks if the user actually sent a YouTube video link
    //////
    Обработчик проверяет действительно ли пользователь отправил ссылку на видео YouTube
    """
    youtube_link = message.text
    print(youtube_link)
    try:
        yt = YouTube(youtube_link)
    except RegexMatchError as r:
        print(r)
        bot.reply_to(message, f'{url_error}')
        bot.register_for_reply(message, callback=start(message))
    bot.register_next_step_handler(message, get_video_resolution)


def get_video_resolution(message):
    """
    Handler, in response to sending the user's URL, ask what resolution quality to download video
    /////
    Обработчик, в ответ на отправку URL пользователя, спрашивает в каком разрешении скачивать видео
    """
    global youtube_link, yt
    youtube_link = message.text
    yt = YouTube(youtube_link)
    kb = types.InlineKeyboardMarkup(row_width=3)
    low_resolution = types.InlineKeyboardButton("Низкое качество", callback_data='low')
    hight_resolution = types.InlineKeyboardButton("Высокое качество", callback_data='hight')
    kb.add(low_resolution, hight_resolution)
    bot.send_message(message.chat.id, video_is_ready, reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: True)
def get_video_from_youtube(callback):
    """
    Handler for downloading video in selected resolution
    /////
    Обработчик для загрузки видео в выбранном разрешении
    """
    try:
        if callback.data == 'low':
            stream = yt.streams.get_lowest_resolution()
            low_quality_video = stream.download("download")
            file = open(f'{low_quality_video}', 'rb')
        elif callback.data == 'hight':
            stream = yt.streams.get_highest_resolution()
            hight_quality_video = stream.download("download")
            file = open(f'{hight_quality_video}', 'rb')
        bot.send_video(callback.message.chat.id, file)
    except Exception:
        bot.send_message(callback.message.chat.id, too_large_file)

    new_url = bot.send_message(callback.message.chat.id, ctn_url)
    bot.register_next_step_handler(new_url, get_video_resolution)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
