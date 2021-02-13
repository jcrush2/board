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
	
	
#@bot.message_handler(func=lambda msg: msg.entities is not None)
#def delete_links(msg):
#	for entity in msg.entities:  # Пройдёмся по всем entities в поисках ссылок
#		if entity.type in ["url", "text_link"]: 
#			bot.delete_message(msg.chat.id, msg.message_id)
#		else:
#			return
			
#@bot.message_handler(func=lambda msg: msg.caption_entities is not None, content_types=["photo"])
#def delete_links(msg):
#	for entity in msg.caption_entities:  # Пройдёмся по всем entities в поисках ссылок
#		if entity.type in ["url", "text_link"]: 
#			bot.delete_message(msg.chat.id, msg.message_id)
#		else:
#			return
		
def otzyv(msg):        
	keyboard = types.InlineKeyboardMarkup()
	url_button = types.InlineKeyboardButton(text=f"Отзывы - {msg.from_user.first_name} 💬", url=f"https://khabara.ru/tg/{msg.from_user.id}-id.html")
	keyboard.add(url_button)
	bot.reply_to(msg, f'ℹ️ Объявление от <a href="tg://user?id={msg.from_user.id}">{msg.from_user.first_name}</a>\n<i>Оставить отзыв ⬇️️️</i>', parse_mode="HTML", reply_markup=keyboard)
			
		
def antispam(msg):
	if msg.caption !=None:
		textspam=msg.caption.lower()
	else:
		textspam=msg.text.lower()

	if textspam is None or 'zwzff' in textspam or 'wa.me' in textspam or 'www' in textspam or 'http' in textspam or 't.me' in textspam or len(textspam) < 4 or re.search('\d', textspam) == None:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:
		for entity in msg.entities:  # Пройдёмся по всем entities в поисках ссылок
			if entity.type in ["url", "text_link"]: 
				bot.delete_message(msg.chat.id, msg.message_id)
			else:
				otzyv(msg)

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
	if msg.forward_from_chat != None:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:
		antispam(msg)
	
@bot.message_handler(content_types=['photo'])	
def karma_game(msg):
	if msg.forward_from_chat != None:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:
		if msg.caption !=None:
			antispam(msg)
		else:
			bot.delete_message(msg.chat.id, msg.message_id)
		
		
@bot.message_handler(content_types=['video'])	
def karma_game(msg):
	if msg.forward_from_chat != None:
		bot.delete_message(msg.chat.id, msg.message_id)
	else:
		if msg.caption !=None:
			antispam(msg)
		else:
			bot.delete_message(msg.chat.id, msg.message_id)
		

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
