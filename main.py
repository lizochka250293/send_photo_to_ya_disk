import os
import shutil
from datetime import datetime
import telebot
import yadisk

from connector import DiskConnector

bot = telebot.TeleBot('5351701742:AAF8F7I44xoGk6rqEAS7WcR_Q4uSxwfWOu8')
photo_list = []
document_list = []
disk = DiskConnector()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Получи и отправь токен https://oauth.yandex.ru/client/new')

@bot.message_handler(commands=['break'])
def send_break(message):
    bot.send_message(message.chat.id, 'Загрузка завершена')
    delete()
    return


@bot.message_handler(content_types=['text'])
def set_token(message):
    token = message.text
    disk.set_token(token)

    if disk.check_token():
        sent = bot.reply_to(message, 'Token is valid! Загружай файл')
        bot.register_next_step_handler(sent, upload_step)
    else:
        sent = bot.reply_to(message, 'Token invalid! Получи и отправь токен https://oauth.yandex.ru/client/new')


@bot.message_handler(content_types=['photo', 'document'])
def upload_step(message):
    if not disk.back(bot, message) and message.content_type in ["text"]:
        sent = bot.reply_to(message, 'Проверь формат файла')
        bot.register_next_step_handler(sent, upload_step)
    elif message.content_type in ["document", "photo"]:
        upload_result = disk.upload(bot, message)
        if upload_result:
            sent = bot.reply_to(message, 'Файл загружен! /break, если загрузка завершена')
            bot.register_next_step_handler(sent, upload_step)
        else:
            sent = bot.reply_to(message, 'Файл не загружен, проверьте формат файла')
            bot.register_next_step_handler(sent, upload_step)

def delete():
    folder = 'C:/Users/bt030/PycharmProjects/send_photo_yandex_disk/files/documents'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    folder = 'C:/Users/bt030/PycharmProjects/send_photo_yandex_disk/files/photos'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    bot.polling(none_stop=True)
    delete()
