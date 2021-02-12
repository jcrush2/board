#!usr/bin/python3
import hashlib
import string
import os
import re

from flask import Flask, request

import telebot

from telebot import types
import config


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

def commands_foto(msg):        
	keyboard = types.InlineKeyboardMarkup()
	url_button = types.InlineKeyboardButton(text=f"Отзывы - {msg.from_user.first_name} 💬", url=f"https://khabara.ru/app/{msg.from_user.id}-comm.html")
	keyboard.add(url_button)
	bot.send_message(msg.chat.id, f'ℹ️ Объявление от <a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name}</a> размещено.\n\nЧтобы откликнуться, пишите автору в <a href="tg://user?id={msg.from_user.id}">📩 личку</a>, или по указанным контактам.\n\n<i>Оставить отзыв можно по кнопке ниже.</i>', parse_mode="HTML", reply_markup=keyboard)
			
def commands(msg, text):
	if forward_from_chat == None:
		bot.delete_message(msg.chat.id, msg.message_id)
	if len(text) < 4:
		bot.delete_message(msg.chat.id, msg.message_id)
	if re.search('\d+', msg.text.lower()) == None:
			bot.delete_message(msg.chat.id, msg.message_id)
	else:
		commands_foto(msg)
#		if re.search(r'^(.*@[a-zA-Z0-9])|((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{6,10}',msg.text.lower())== None:
#			bot.send_message(msg.chat.id, f"🗑 Объявление от <b>{msg.from_user.first_name}</b> удаленно, т.к. не содержит контактной информации. Для общения в свободной форме: @KhvChat", parse_mode="HTML")

def commands_media(msg):
	if forward_from_chat == None:
		bot.delete_message(msg.chat.id, msg.message_id)
	if msg.caption is None:
		bot.delete_message(msg.chat.id, msg.message_id)
	if len(msg.caption) < 4:
		bot.delete_message(msg.chat.id, msg.message_id)
	if re.search('\d+', msg.caption.lower()) == None:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:
		commands_foto(msg)

def reply_exist(msg):
	return msg.reply_to_message


@bot.message_handler(content_types=["text"], func=reply_exist)
def changing_karma_text(msg):
	bot.delete_message(msg.chat.id, msg.message_id)
	
@bot.message_handler(content_types=["photo"], func=reply_exist)
def changing_karma_text(msg):
	bot.delete_message(msg.chat.id, msg.message_id)
	
@bot.message_handler(content_types=["video"], func=reply_exist)
def changing_karma_text(msg):
	bot.delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(content_types=['text'])	
def karma_game(msg):

	commands(msg, msg.text)
	
@bot.message_handler(content_types=['photo'])	
def karma_game(msg):
	commands_media(msg)
		
@bot.message_handler(content_types=['video'])	
def karma_game(msg):
	commands_media(msg)
		

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
