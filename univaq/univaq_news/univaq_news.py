#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from utils import utils
from bs4   import BeautifulSoup

prefix_univaq = 'http://www.univaq.it/'
url_evidenza = 'http://www.univaq.it/news_archive.php?tipo=In%20evidenza'
url_ultimissime = 'http://www.univaq.it/news_archive.php?tipo=Ultimissime'

lista_univaq = utils.get_list(2)

lista_ultimissime = []
lista_evidenza = []
dictionary = {}

#Filling data structures.

def preparing_univaq():
    global lista_evidenza
    global lista_ultimissime
    global dictionary

    univaq_evidenza = utils.get_news(url_evidenza).find_all('div', 'allegati')
    univaq_ultimissime = utils.get_news(url_ultimissime).find_all('div', 'allegati')

    for element in univaq_evidenza:
        lista_evidenza.append(element.next_sibling.next_sibling.get_text())
    for element in univaq_ultimissime:
        lista_ultimissime.append(element.next_sibling.next_sibling.get_text())
    dictionary = {1:lista_evidenza, 2:lista_ultimissime}

#The following function shows the last 5 news from univaq site --> evidenza section

def evidenza(bot, update):
    univaq_site = utils.get_news(url_evidenza).find_all('div', 'allegati')[0:5]
    text = ''
    for i, element in enumerate(univaq_site):
        text += ('{} - '.format(i+1) +
                 '<a href=\'' + prefix_univaq +
                 element.next_sibling.next_sibling['href'] + '\'>' +
                 element.next_sibling.next_sibling.get_text() + '</a>\n\n')
    text += '<i>Queste sono le notizie relative alla sezione \"In Evidenza\".</i>'

    if update.message.chat_id not in lista_univaq:
        text += '\n\n<b>Abilita le notifiche con il comando</b> /univaqon <b>se vuoi restare aggiornato!</b>'
    bot.sendMessage(update.message.chat_id, utils.text_cleanup(text), parse_mode='HTML', disable_web_page_preview=True)

#The following function shows the last 5 news from univaq site --> ultimissime section

def ultimissime(bot, update):
    univaq_site = utils.get_news(url_ultimissime).find_all('div', 'allegati')[0:5]
    text = ''
    for i, element in enumerate(univaq_site):
        text += ('{} - '.format(i+1) +
                 '<a href=\'' + prefix_univaq +
                 element.next_sibling.next_sibling['href'] + '\'>' +
                 element.next_sibling.next_sibling.get_text() + '</a>\n\n')
    text += '<i>Queste sono le notizie relative alla sezione \"Ultimissime\".</i>'

    if update.message.chat_id not in lista_univaq:
        text += '\n\n<b>Abilita le notifiche con il comando</b> /univaqon <b>se vuoi restare aggiornato!</b>'
    bot.sendMessage(update.message.chat_id, utils.text_cleanup(text), parse_mode='HTML', disable_web_page_preview=True)

#The following function enables the notifications for Univaq news.

def univaqon(bot, update):
    if update.message.chat_id not in lista_univaq:
        lista_univaq.append(update.message.chat_id)
        utils.append_in_list(update.message.chat_id, 2)
        bot.sendMessage(update.message.chat_id, 'Le notifiche relative all\'Univaq sono abilitate!')
        return
    bot.sendMessage(update.message.chat_id, 'Le notifiche relative all\'Univaq sono già abilitate!')

#The following function disables the notifications for Univaq news.

def univaqoff(bot, update):
    if update.message.chat_id in lista_univaq:
        lista_univaq.remove(update.message.chat_id)
        utils.save_list(lista_univaq, 2)
        bot.sendMessage(update.message.chat_id, 'Le notifiche relative all\'Univaq sono disattivate!')
        return
    bot.sendMessage(update.message.chat_id, 'Le notifiche relative all\'Univaq sono già disattivate!')

#The following function is a general procedure to check news in Evidenza e Ultimissime sections.

def general_news_check(bot, pagina, index):
    if lista_univaq == []:
        return
    try:
        web_page = urllib2.urlopen(pagina)
        soup = BeautifulSoup(web_page, 'lxml')
        news = soup.find_all('div', 'allegati')
    except:
        return
    global dictionary
    temp = []
    messaggi = []
    if index == 1:
        sezione = '<i>In Evidenza:</i>'
    else:
        sezione = '<i>Ultimissime:</i>'
    #Looking for new announcementes on Univaq site.
    for element in news[0:5]:
        if element.next_sibling.next_sibling.get_text() not in dictionary[index]:
            messaggi.append(sezione +
                            '\n<a href=\'' + prefix_univaq +
                            element.next_sibling.next_sibling['href'] + '\'>' +
                            element.next_sibling.next_sibling.get_text() + '</a>')
    if messaggi == []:
        return
    #Sending new announcementes(if existing) to users.
    for person in lista_univaq:
        for element in messaggi[::-1]:
            try:
                bot.sendMessage(person, utils.text_cleanup(element), parse_mode='HTML')
            except:
                temp.append(person)
                break
    if temp != []:
        for element in temp:
            lista_univaq.remove(element)
        utils.save_list(lista_univaq, 2)
    dictionary[index] = []
    #Updating data structures in case of new announcementes.
    for element in news:
        dictionary[index].append(element.next_sibling.next_sibling.get_text())

#The following function is launched from main function each minute and thirty seconds.
#The function's aim is to check for new announcementes on Univaq site and if so, send them to users and updates data structures(dictionary, lists, ...).

def check_univaq_news(bot, job):
    general_news_check(bot, url_evidenza, 1)
    general_news_check(bot, url_ultimissime, 2)
