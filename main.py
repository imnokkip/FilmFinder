import telebot
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import config

bot = telebot.TeleBot(config.TOKEN)

URL = 'https://www.kinopoisk.ru/index.php?kp_query='

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie': f'{config.COOKIE}',
    'User-Agent': f'{generate_user_agent()}'
}


class BotStarter:
    def __init__(self):
		bot.polling(none_stop=True, interval=0)

    @staticmethod
    def check(name):
        pic = []
        film_title = []
        other = []
        film_id = []

        html = requests.get(f'{URL}{name}', headers=headers)
        html = BeautifulSoup(html.text, 'lxml')

        for cards in html.find_all('div', 'search_results'):
            if cards != html.find_all('', 'search_results')[-1]:
                for cards_data in cards.find_all('div', 'element'):
                    film_title.append(cards_data.find('p', 'name').get_text())
                    other.append(cards_data.find_all('span', 'gray')[0].get_text())
                    film_id.append(cards_data.find('p', 'pic').find('a', 'js-serp-metrika').get('data-url').strip('/film/'))

        return pic, film_title, other, film_id

    @staticmethod
    def get_img(ids):
        html = requests.get(f'{"https://1ww.frkp.live/?id="}{ids}/', headers=headers)
        html = BeautifulSoup(html.text, 'lxml')
        return html.find('div', 'webr').find('img').get('src')

    @bot.message_handler(commands=['start'])
    def start_msg(message):
        bot.send_message(message.chat.id, f'Hello {message.from_user.username}!')

 @bot.message_handler(commands=['find'])
    def finder(message):
        pic, film_title, other, film_id = BotStarter.check(message.text.strip('/find '))
        for a in range(len(film_id)):
            if other[a] '':
                bot.send_photo(message.chat.id, photo=BotStarter.get_img(film_id[a]),
 caption=f'{a+1})ильм:\nНазвание: {film_title[a]}\nВремя: {other[a]}\nID: {film_id[a]} Ссылка на Кинопоиск: https://www.kinopoisk.ru/series/{film_id}/')

    @bot.message_handler()
 def i_dont(message):
        bot.reply_to(message, 'Простите я не понимаю это...')
        print(message.text)


if __name__ == '__main__':
    started = BotStarter()
