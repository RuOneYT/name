from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import requests
from bs4 import BeautifulSoup as bs4
from kinopoisk.movie import Movie


updater = Updater(token="968621763:AAGx81FOL1oklcFdGVpBO1z4UdZe4_8fkNw", use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format= ' %(asctime)s- %(name)s- %(levelname)s- %(message)s ',
                    level= logging.INFO)
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введи /start.')
    

def start( update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Привет я бот для поиска фильмов.Введи /search затем название фильма или мультсериала...")


def search(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = 'Ищу для вас информацию')
    a = ' '.join(context.args)
    movie_list = Movie.objects.search(a)
    movie = Movie(id = movie_list[0].id)
    movie.get_content("main_page")
    movie.get_content('posters')
    posters = movie.posters
    context.bot.send_photo(chat_id= update.effective_chat.id, photo=posters[0])
    movie.plot
    b = movie.plot
    url = "https://kinopoisk.ru/film/" + str(movie_list[0].id)
    context.bot.send_message(chat_id=update.effective_chat.id, text = b)
    context.bot.send_message(chat_id=update.effective_chat.id, text = f'Ссылка на фильм:{url}')

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

search_handler = MessageHandler(Filters.text, search)
dispatcher.add_handler(search_handler)

search_handler = CommandHandler('search', search)
dispatcher.add_handler(search_handler)

updater.start_polling()