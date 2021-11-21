import config
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from pygtrans import Translate

URL1 = 'http://russian-poetry.ru/Random.php'
URL2 = 'https://www.generatormix.com/random-compliment-generator'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
	'Accept': '*/*'
}
client = Translate()

#Parser


def get_poem(html):
	global poems
	soup = BeautifulSoup(html, 'html.parser')
	poems = soup.find("pre").find(text=True)
	print(soup)


def parse_poem(url, params=None):
	html = requests.get(url, headers=HEADERS, params=params)
	if html.status_code == 200:
		get_poem(html.text)
	else:
		print('error')

def get_complimet(html):
	global complimets
	soup = BeautifulSoup(html, 'html.parser')
	complimets = soup.find("blockquote", class_ = 'text-left').get_text()


def parse_complimet(url, params=None):
	html = requests.get(url, headers=HEADERS, params=params)
	if html.status_code == 200:
		get_complimet(html.text)
	else:
		print('error')

parse_complimet(URL2)

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

"""#  echo
@dp.message_handler()
async def echo(message: types.Message):
	await message.answer(message.text)
"""
@dp.message_handler(commands = ['start'])
async def start_message(message: types.Message):
	await bot.send_message(message.from_user.id, """ Привет я твой личный Купибот, я создан для того чтобы поднять тебе настроение:
ты можешь просто написать, что хочешь стих или комплимент и я тебе его напишу!""")

@dp.message_handler()
async def poem(message: types.Message):
	if "стих" in message.text:
		parse_poem(URL1)
		parse_complimet(URL2)
		await bot.send_message(message.from_user.id, poems)
	elif "комплимент" in message.text:
		parse_complimet(URL2)
		text = client.translate(complimets , target='ru')
		await bot.send_message(message.from_user.id, text.translatedText)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)