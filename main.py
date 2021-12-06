# -*- coding: utf-8 -*-
import telebot
import database
from config import bot_token, admin_id
from telebot import types
import re
import json
import secrets

db = database.DataBase()
bot = telebot.TeleBot(bot_token,parse_mode='Markdown')

import hashlib


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == '❌ Отмена')
@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def start(message):
    print(message.chat.id)
    if not db.get_user(message.chat.id):
        return
    else:

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🌟 Избранные', '📃 Создать пост')
        if admin_id == message.chat.id:
            markup.row('🔐 Добавить id')
        if message.text == '❌ Отмена' or message.text == '⬅️ Назад':
            bot.send_message(message.chat.id, "Главное меню ", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Привет, пользователь!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🔐 Добавить id')
def add_telegram_id_info(message):
    if message.chat.id == admin_id:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('❌ Отмена')
        bot.send_message(message.chat.id, 'Введите ид юзера', reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: add_telegram_id(m))

    else:
        bot.send_message(message.chat.id, 'Призойшла ошибка')


def add_telegram_id(message):
    if message.text == '❌ Отмена':
        start(message)
        return

    try:
        db.insert_telegram_id(message.text)
        bot.send_message(message.chat.id, 'Добавлен id - {} '.format(message.text))
        start(message)
    except:
        bot.send_message(message.chat.id, 'Введите правильно ид')
        bot.register_next_step_handler(message, lambda m: add_telegram_id(m))
        return
        
   bot.polling(none_stop=True)
     
