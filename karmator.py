#!usr/bin/python3
import datetime
import hashlib
import string
import os
import random
import requests
import json
import re

from flask import Flask, request

import telebot
from logger import main_log
from telebot import types
import config

main_log.info("Program starting")
TELEGRAM_API = os.environ["telegram_token"]
bot = telebot.TeleBot(TELEGRAM_API)

def is_my_message(msg):
	"""
	Функция для проверки, какому боту отправлено сообщение.
	Для того, чтобы не реагировать на команды для других ботов.
	:param msg: Объект сообщения, для которого проводится проверка.
	"""
	text = msg.text.split()[0].split("@")
	if len(text) > 1:
		if text[1] != config.bot_name:
			return False
	return True


@bot.message_handler(commands=["start"], func=is_my_message)
def start(msg):
	"""
	Функция для ответа на сообщение-команду для приветствия пользователя.
	:param msg: Объект сообщения-команды
	"""


	reply_text = (
			"Здравствуйте, я бот, который отвечает за " +
			" подсчет кармы в чате @khvchat.")
	bot.send_message(msg.chat.id, reply_text)


			
def commands(msg, text):
	main_log.info("Starting func 'commands'")
	if len(text) < 4:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:

		keyboard = types.InlineKeyboardMarkup()
		url_button = types.InlineKeyboardButton(text="Написать", url="tg://user?id="+msg.from_user.id)
		url_button2 = types.InlineKeyboardButton(text="Оставить отзыв", url="https://www.aviasales.ru/search/KHV")
		keyboard.add(url_button,url_button2)
		bot.send_message(msg.chat.id, f'🐊 {msg.from_user.first_name} разместил объявление.', reply_markup=keyboard)

	if re.search(r'[а-яА-ЯёЁ]',msg.text.split()[0].lower()) and re.search(r'[A-Za-z]',msg.text.split()[0].lower()):
		bot.reply_to(msg,f"Попытался обойти систему 🗿", parse_mode="HTML")
		
	if msg.text.lower() == seves:
		if seves_id ==  f"{msg.from_user.id}":
					bot.send_chat_action(msg.chat.id, "typing")
					bot.reply_to(msg,f"Мухлевать не красиво: -10 кармы 💩", parse_mode="HTML")
					change_karma(msg.from_user, msg.chat, -10)
					
		else:
			bot.send_chat_action(msg.chat.id, "typing")
			bot.reply_to(msg,f"🎉 Правильный ответ: <b>{seves}</b> +3 кармы, запустить игру /croco", parse_mode="HTML")
			change_karma(msg.from_user, msg.chat, 3)
			saves_database[database] = "dse4f"



def reply_exist(msg):
	return msg.reply_to_message


@bot.message_handler(content_types=["text"], func=reply_exist)
def changing_karma_text(msg):
	bot.delete_message(msg.chat.id, msg.message_id)
	commands(msg, msg.text)
	

	
@bot.message_handler(content_types=['text'])	
def karma_game(msg):

	commands(msg, msg.text)

				
				



# Дальнейший код используется для установки и удаления вебхуков
server = Flask(__name__)


@server.route("/bot", methods=['POST'])
def get_message():
	""" TODO """
	decode_json = request.stream.read().decode("utf-8")
	bot.process_new_updates([telebot.types.Update.de_json(decode_json)])
	return "!", 200


@server.route("/")
def webhook_add():
	""" TODO """
	bot.remove_webhook()
	bot.set_webhook(url=config.url)
	return "!", 200

@server.route("/<password>")
def webhook_rem(password):
	""" TODO """
	password_hash = hashlib.md5(bytes(password, encoding="utf-8")).hexdigest()
	if password_hash == "5b4ae01462b2930e129e31636e2fdb68":
		bot.remove_webhook()
		return "Webhook removed", 200
	else:
		return "Invalid password", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
