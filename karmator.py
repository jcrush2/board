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


			
def commands(msg, text):
	


	if 'бот ' in msg.text.lower() or ' бот' in msg.text.lower() or 'скуч' in msg.text.lower():
		bot.send_chat_action(msg.chat.id, "typing")
		bot.reply_to(msg, f"{random.choice(config.bot_words)}", parse_mode="HTML")

	if 'бот фильм' in msg.text.lower() or ' бот фильм' in msg.text.lower():
		bot.send_chat_action(msg.chat.id, "typing")
		bot.reply_to(msg, f"{random.choice(config.bot_film)}", parse_mode="HTML")

	if '!? ' in msg.text.lower():
		bot.send_chat_action(msg.chat.id, "typing")
		random_karma = ("Абсолютно точно!","Да.","Нет.","Скорее да, чем нет.","Не уверен...","Однозначно нет!","Если ты не фанат аниме, у тебя все получится!","Можешь быть уверен в этом.","Перспективы не очень хорошие.","А как же иначе?.","Да, но если только ты не смотришь аниме.","Знаки говорят - да.","Не знаю.","Мой ответ - нет.","Весьма сомнительно.","Не могу дать точный ответ.")
		random_karma2 = random.choice(random_karma)
		bot.reply_to(msg, f"🔮 {random_karma2}", parse_mode="HTML")
	if '!v ' in msg.text.lower():
		result = msg.text.lower()
		result = result.replace(msg.text.split()[0], "")
		bot.send_poll(msg.chat.id, f'{result}❓', ['Да!', 'Нет.', 'Не знаю.'])
		
	if ' vs ' in msg.text.lower():
		bot.send_chat_action(msg.chat.id, "typing")
		random_karma = ("2️⃣ Определенно второе","1️⃣ Определенно первое")
		random_karma2 = random.choice(random_karma)
		bot.reply_to(msg, f"🔮 {random_karma2}", parse_mode="HTML")
		
	if 'love' in msg.text.lower():
		loves_text = "<a href='tg://user?id=55910350'>❤</a>️ Ваше объявление будет размещено в Знакомствах: @love_khv"
		bot.reply_to(msg, loves_text, parse_mode="HTML")
	
	if msg.text.lower() in ['язабан']:
		user = bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
		if user.status == 'administrator' or user.status == 'creator':
			return
		if msg.reply_to_message:
			bot.send_message(msg.chat.id, f"<a href='tg://user?id=55910350'>🔫</a> <b>{msg.from_user.first_name}</b> предлагает выгнать <b>{msg.reply_to_message.from_user.first_name}</b> из Хабчата!", parse_mode="HTML")
			bot.send_poll(msg.chat.id, f'Согласны выгнать {msg.reply_to_message.from_user.first_name} из Чата?', ['Да', 'Нет', 'Не знаю'],is_anonymous=False)
		else:
			return
	
	if msg.text.lower() in ['!k']:
		bot.delete_message(msg.chat.id, msg.message_id)
		user = bot.get_chat_member(msg.chat.id, msg.from_user.id)
		if user.status == 'creator':
			krasavchik(msg)

	if msg.text.lower() in ['цитата']:
		citata = random.choice(config.citata_words)
		bot.send_chat_action(msg.chat.id, "typing")
		bot.reply_to(msg, f"📍 Цитата: {citata}", parse_mode="HTML")
		
	if msg.text.lower() in ['билет']:
		bot.send_chat_action(msg.chat.id, "typing")
		url = "https://api.travelpayouts.com/v1/prices/cheap"
		querystring = {"origin":"KHV","destination":"-","depart_date":"2021-01"}
		headers = {'x-access-token': '83a5fe66f97a36e6f0be4b2be21a5552'}
		response = requests.request("GET", url, headers=headers, params=querystring)
#		bot.reply_to(msg, f"📍 Цитата: {response.text}", parse_mode="HTML")
		data = response.json()
		a1 = data['data']['BKK']['1']['price']
		a2 = data['data']['AER']['1']['price']
		t2 = data['data']['AER']['1']['expires_at']
		bot.reply_to(msg, f"✈️ Бангкок (Таиланд), цена: {a1}", parse_mode="HTML")
		bot.reply_to(msg, f"✈️ Сочи (Адлер), цена: {a2}", parse_mode="HTML")
		keyboard = types.InlineKeyboardMarkup()
		url_button = types.InlineKeyboardButton(text="Посмотреть", url="https://www.aviasales.ru/search/KHV"+t2+"AER1")
		keyboard.add(url_button)
		bot.send_message(msg.chat.id, "Вы можете купить билет, оплатив по кнопке ниже.", reply_markup=keyboard)
		
	if msg.text.lower() in ['купить']:
		keyboard = types.InlineKeyboardMarkup()
		url_button = types.InlineKeyboardButton(text="💰 Купить кармы - 1р.", url="https://khabara.ru/informer.html")
		keyboard.add(url_button)
		bot.send_message(msg.chat.id, "Вы можете купить карму, оплатив по кнопке ниже.", reply_markup=keyboard)
		
	if ' чат ' in msg.text.lower():
		keyboard = types.InlineKeyboardMarkup()
		url_button1 = types.InlineKeyboardButton(text="TG", url="https://t.me/share/url?url=t.me/khvchat&text=Привет! Мы общаемся в Чате Хабаровска в Telegram, заходи к нам: https://t.me/khvchat")
		url_button2 = types.InlineKeyboardButton(text="WA", url="https://api.whatsapp.com/send?text=Привет! Мы общаемся в Чате Хабаровска в Telegram, заходи к нам: https://t.me/khvchat")
		url_button3 = types.InlineKeyboardButton(text="ВК", url="https://vk.com/share.php?url=https://t.me/khvchat&title=Привет! Мы общаемся в Чате Хабаровска в Telegram, заходи к нам: https://t.me/khvchat")
		
		url_button4 = types.InlineKeyboardButton(text="ОК", url="https://connect.ok.ru/offer?url=https://t.me/khvchat&title=Привет! Мы общаемся в Чате Хабаровска в Telegram, заходи к нам: https://t.me/khvchat")
		
		keyboard.row(url_button1, url_button2, url_button3, url_button4)
		bot.send_message(msg.chat.id, "💬 Пригласи в ХабЧат друзей из других мессенджеров:", reply_markup=keyboard)
		
		
	if msg.text.lower() in ['утра']:
		bot.send_chat_action(msg.chat.id, "typing")
		citata = random.choice(config.citata_words)
		bot.reply_to(msg, f"С добрым утром, Хабаровск! ☀️ Вам отличного и позитивного настроения!!!", parse_mode="HTML")

	if msg.text.lower() in ['превед']:
		if msg.reply_to_message:
			bot.send_chat_action(msg.chat.id, "typing")
			bot.reply_to(msg.reply_to_message,f"✌Приветствуем тебя в <b>ХабЧате</b>! По доброй традиции, желательно представиться и рассказать немного о себе.", parse_mode="HTML")
		else:
			return
	if msg.text.lower() in ['сохранить'] or msg.text.lower() in ['save']:
		if msg.reply_to_message:
			bot.send_chat_action(msg.chat.id, "typing")
			bot.forward_message(-1001338159710, msg.chat.id, msg.reply_to_message.message_id)
			bot.reply_to(msg.reply_to_message,f"💾 Сообщение сохранено в <a href='https://t.me/joinchat/T8KyXgxSk1o4s7Hk'>Цитатник ХабЧата</a>.", parse_mode="HTML")
		else:
			return
	if msg.text.lower() in ['фото']:
		if msg.reply_to_message:
			bot.send_chat_action(msg.chat.id, "typing")
			bot.reply_to(msg.reply_to_message,f"Не соблаговолите ли вы скинуть в чат свою фоточку, нам будет очень приятно вас лицезреть 🙂", parse_mode="HTML")
		else:
			return
	if msg.text.lower() in ['фсб']:
		if msg.reply_to_message:
			bot.send_chat_action(msg.chat.id, "typing")
			bot.reply_to(msg.reply_to_message,f"<a href='https://telegra.ph/file/1a296399c86ac7a19777f.jpg'>😎</a> За вами уже выехали!", parse_mode="HTML")
		else:
			return
	if msg.text.lower() in ['войс']:
		if msg.reply_to_message:
			bot.reply_to(msg.reply_to_message,f"🔔🔔🔔🔔🔔🔔🔔\n🗣Го в Войс Чат!👂\
\n🔔🔔🔔🔔🔔🔔🔔", parse_mode="HTML")
		else:
			bot.send_message(msg.chat.id, f"🔔🔔🔔🔔🔔🔔🔔\n🗣Го в Войс Чат!👂\
\n🔔🔔🔔🔔🔔🔔🔔", parse_mode="HTML")

	if '!к ' in msg.text.lower():
		
		result = msg.text.split()[1].lower()
		bot.send_message(msg.chat.id,f'🐊 {msg.from_user.first_name} загадал(а) свое слово.', parse_mode="HTML")
		saves_database[database] = result
		bot.send_message(-1001110839896,f'🐊 {msg.from_user.first_name} загадал(а) свое слово.', parse_mode="HTML")
#		bot.forward_message(-1001110839896, msg.message_id)
		bot.delete_message(msg.chat.id, msg.message_id)

	if msg.text.lower() in ['крокодил'] or msg.text.lower() in ['/croco@khabara_bot']:
		saves_database_id[database_id] =f"{msg.from_user.id}"
		saves_database[database] = random.choice(config.kroko_words)
		bot.send_chat_action(msg.chat.id, "typing")
		markup = telebot.types.InlineKeyboardMarkup()
		button = telebot.types.InlineKeyboardButton(text='Посмотреть слово', callback_data=msg.from_user.id)
		button2 = telebot.types.InlineKeyboardButton(text='Сменить слово', callback_data=msg.from_user.first_name)
		markup.add(button,button2)
		bot.send_message(chat_id=msg.chat.id, text=f'🐊 {msg.from_user.first_name} загадал(а) слово.', reply_markup=markup)
	seves = saves_database.get(database)
	seves_id = saves_database_id.get(database_id)

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
