#!usr/bin/python3
import hashlib
import string
import os

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

def commands_foto(msg):
	keyboard = types.InlineKeyboardMarkup()
	url_button = types.InlineKeyboardButton(text="Отзывы 💬", url=f"https://khabara.ru/app/{msg.from_user.id}-comm.html&{msg.from_user.first_name}")
	keyboard.add(url_button)
	bot.send_message(msg.chat.id, f'ℹ️ <b>{msg.from_user.first_name}</b> разместил объявление.\n\nЧтобы откликнуться, непишите ему в <a href="tg://user?id={msg.from_user.id}">📩 личу</a>, или по его контактам.\n\n<i>Оставить отзыв о продавце можно по кнопке ниже.</i>', parse_mode="HTML", reply_markup=keyboard)
			
def commands(msg, text):
	main_log.info("Starting func 'commands'")
	if len(text) < 4:
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
	

	


@bot.message_handler(content_types=['photo'])	
def karma_game(msg):
	commands_foto(msg)
	
@bot.message_handler(content_types=['video'])	
def karma_game(msg):
	commands_foto(msg)

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
