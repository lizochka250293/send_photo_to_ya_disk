from datetime import datetime
import os
import shutil
import telebot
import yadisk

bot = telebot.TeleBot('5351701742:AAF8F7I44xoGk6rqEAS7WcR_Q4uSxwfWOu8')
photo_list = []
document_list = []
token_list = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Получи и отправь токен https://oauth.yandex.ru/client/new')



@bot.message_handler(content_types=['text'])
def token(message):
    token = message.text
    token_list.append(token)
    print(token_list)
    bot.send_message(message.chat.id, 'Отправьте файл для загрузки')


@bot.message_handler(content_types=['photo', 'document'])
def upload_step(message):
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    if message.content_type == "document":
        if message.document.file_id not in document_list:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            document_list.append(message.document.file_id)
            print(document_list)
            src = 'files/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                path = new_file.name.split("/")
                file_to_path = "{}.{}".format(date, path[2])
                for i in token_list:
                    token = i
                y = yadisk.YaDisk(token=token)
                try:
                    y.mkdir("/telegram")
                    try:
                        y.check_token()
                    except yadisk.exceptions.UnauthorizedError:
                        bot.reply_to(message, "Проверь токен")
                    else:
                        y.upload(f"{src}", f"/telegram/{file_to_path}")
                        bot.reply_to(message, "Пожалуй, я сохраню это")
                except:
                    try:
                        y.check_token()
                    except Exception as e:
                        bot.reply_to(message, e)
                    else:
                        y.upload(f"{src}", f"/telegram/{file_to_path}")
                        bot.reply_to(message, "Пожалуй, я сохраню это")

    elif message.content_type == "photo":
        if message.photo[-1].file_id not in photo_list:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            photo_list.append(message.photo[-1].file_id)
            print(photo_list)
            src = 'files/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                path = new_file.name.split("/")
                file_to_path = "{}.{}".format(date, path[2])
                for i in token_list:
                    token = i
                y = yadisk.YaDisk(token=token)
                try:
                    y.mkdir("/telegram")
                    try:
                        y.check_token()
                    except Exception as e:
                        bot.reply_to(message, e)
                    else:
                        y.upload(f"{src}", f"/telegram/{file_to_path}")
                except:
                    try:
                        y.check_token()
                    except yadisk.exceptions.UnauthorizedError:
                        bot.reply_to(message, "Проверь токен")
                    else:
                        y.upload(f"{src}", f"/telegram/{file_to_path}")
                        bot.reply_to(message, "Пожалуй, я сохраню это")


bot.polling()
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
delete()
# y = yadisk.YaDisk(token="AQAAAAACqMGvAAfkuMxxMfH-C0uPp9O6eNnSQ54")
# print(y.check_token())
# # y.mkdir("/test") # Создать папку
# y.upload("text.txt", "/test/file1.txt")
