import json
from time import sleep

from telebot import types
import telebot


bot = telebot.TeleBot('7263442278:AAFCUcEdutpxcDIdyuFhduEscocmW4_rJ0Q')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Получаем файл
    file_info = bot.get_file(message.document.file_id)
    file_downloaded = bot.download_file(file_info.file_path)

    # Сохраняем файл временно
    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(file_downloaded)

    # Читаем содержимое файла и отправляем текст пользователю
    with open(message.document.file_name, 'r', encoding='utf-8') as file:
        text = json.load(file)
        text.reverse()
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Удалить сообщение", callback_data=message.message_id)
        keyboard.add(button)
        for el in text:
            if 'Сезон' in el or 'Выбор на время:' in el or 'Дополнительный выбор:' in el:
                bot.send_message(message.chat.id, f'<b>{el}</b>', parse_mode='html', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, el, reply_markup=keyboard)
            sleep(0.2)

from os import system
# Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_delete_message(call):
    # Получаем ID сообщения, которое нужно удалить
    # Удаляем сообщение
    bot.delete_message(call.message.chat.id, call.message.id)

print('Бот запущен')
bot.polling(non_stop=True, interval=0) #запуск бота
print('Бот отключён')
