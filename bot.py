import telebot
from path import Path
import time

from generator_qr import qr_code

token = '#'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне сначала картинку, а потом текст и я сделаю из этого QR-Code!")


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    global path_to_download
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path
        print(src)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        path_to_download = Path().joinpath(src)
        bot.reply_to(message, "Фото получено! Отправьте текст!")

    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global path_to_download
    try:
        tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
        msg = tconv(message.date)
        file_name = str(message.from_user.first_name)
        with open('URL_DATA.txt', 'a') as file:
            file.write(message.text + '  ' + file_name + ' ' + msg + '\n')
        bot.reply_to(message, 'Ваш текст принят!\nОжидайте.')
        qr_code(message.text, path_to_download)
        with open('qr_code.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, 'Ваш QR-Code готов!')

    except Exception:
        bot.reply_to(message, "Привет! Пришли мне сначала картинку, а потом текст и я сделаю из этого QR-Code!")


bot.infinity_polling()
