import telebot
from telebot import types
from pytube import YouTube

from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.reply_to(message, start_message)
    bot.register_next_step_handler(sent, get_resolution_list)


def get_resolution_list(message):
    message_to_save = message.text
    yt = YouTube(message_to_save)
    kb = types.InlineKeyboardMarkup(row_width=3)
    resolution_list = yt.streams.filter(file_extension="mp4", type="video", progressive=True)
    for i in resolution_list:
        btn = types.InlineKeyboardButton(f'{i.resolution} {i.fps}fps', callback_data="!!!")
        kb.add(btn)
    bot.send_message(message.chat.id, choose_resolution_message, reply_markup=kb)
#
# def download_video():
#     if btn == "Yes":
#         print("Yes")


@bot.callback_query_handler(func=lambda callback:True)
def check_callback_data(callback):
    if callback.data == "!!!":
        bot.send_message(callback.message.chat.id, "Some_string")



    # change_resolution = input("Change resolution: ")
    # qual = yt.streams.filter(res=f'{change_resolution}').first()
    # print(qual)


# if __name__ == "__main__":
bot.polling(none_stop=True)
