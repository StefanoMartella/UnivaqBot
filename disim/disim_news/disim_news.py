#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from bs4     import BeautifulSoup
from utils   import utils

prefix_disim = 'http://www.disim.univaq.it/main/{}'
disim = 'http://www.disim.univaq.it/main/news.php?entrant={}'

lista_disim = utils.get_list(1)
lista_annunci = []
dictionary = {}

#Filling data structures.

def preparing_disim():
    global lista_annunci
    global dictionary

    annunci_disim = utils.get_news(disim).find_all('div', 'post_item_list')
    annunci_disim2 = utils.get_news(disim, 2).find_all('div', 'post_item_list')

    for element in annunci_disim + annunci_disim2:
        lista_annunci.append(element.a['href'])
    for i, element in enumerate(annunci_disim + annunci_disim2):
        dictionary[lista_annunci[i]] = element.find('p', 'post_description')

#This function shows Disim news.

def show_disim_news(bot, update, args):
    try:
        #News's numbers is fixed to 15 becouse Telegram gave a message size limit.
        if args != [] and int(args[0]) > 15:
            bot.sendMessage(update.message.chat_id, 'Puoi visualizzare al massimo le ultime 15 news.')
            return
    except:
        bot.sendMessage(update.message.chat_id, 'Ops! Dopo il comando /disim puoi inserire solo un numero compreso tra 1 e 15.')
        return
    if args == []:
        index = 5
    else:
        index = int(args[0])
    text = ''
    entrant = 0
    count = 0
    if (index % 5) == 0:
        entrant = (index / 5) + 1
    else:
        entrant = int(round(index / 5 + 2))
    for element in range(1, entrant):
        announcementes = utils.get_news(disim, element).find_all('div', 'post_item_list')
        for news in announcementes:
            if count < index:
                text += ('{} - '.format(count+1) +
                         '<a href=\'{}\'>'.format(prefix_disim.format('') +
                         news.a['href']) +
                         news.a.string  +
                         '</a>:\n<i>' + news.find('p', 'post_description').string.replace('\n', ' ') + '</i>\n\n')
                count += 1
            else:
                break
    if update.message.chat_id not in lista_disim:
        text += '<b>Abilita le notifiche con il comando</b> /newson <b>se vuoi restare aggiornato!</b>'
    bot.sendMessage(update.message.chat_id, utils.text_cleanup(text), disable_web_page_preview=True, parse_mode='HTML')

#This function enables the notifications for Disim news.

def disimon(bot, update):
    if update.message.chat_id not in lista_disim:
        lista_disim.append(update.message.chat_id)
        utils.append_in_list(update.message.chat_id, 1)
        bot.sendMessage(update.message.chat_id, 'Le notifiche relative al Disim sono abilitate!')
        return
    bot.sendMessage(update.message.chat_id, 'Le notifiche relative al Disim sono già abilitate!')

#This function disables the notifications for Disim news.

def disimoff(bot, update):
    if update.message.chat_id in lista_disim:
        lista_disim.remove(update.message.chat_id)
        utils.save_list(lista_disim, 1)
        bot.sendMessage(update.message.chat_id, 'Le notifiche relative al Disim sono disattivate!')
        return
    bot.sendMessage(update.message.chat_id, 'Le notifiche relative al Disim sono già disattivate!')

#The following function is launched from main function each five minutes and thirty seconds.
#The function's aim is to check for new announcementes on Disim site and if so, send them to users and updates data structures(dictionary, lists, ...).

def check_disim_news(bot, job):
    if lista_disim == []:
        return
    try:
        web_page = urllib2.urlopen(disim.format(1))
        soup = BeautifulSoup(web_page, 'lxml')
        news = soup.find_all('div', 'post_item_list')
    except:
        return
    global dictionary
    global lista_annunci
    temp = []
    messaggi = []
    #Looking for new announcementes on Disim site.
    for element in news:
        if element.a['href'] not in dictionary:
            messaggi.append('<a href=\'{}\'>'.format(prefix_disim.format('') +
                             element.a['href']) + element.a.string + '</a>:\n<i>' +
                             element.find('p', 'post_description').string.replace('\n', ' ') + '</i>')

        elif element.find('p', 'post_description') != dictionary[element.a['href']]:
            messaggi.append('<a href=\'{}\'>'.format(prefix_disim.format('') +
                            element.a['href']) + element.a.string + '</a>:\n<i>' +
                            element.find('p', 'post_description').string.replace('\n', ' ') + '</i>')
    if messaggi == []:
        return
    #Sending new announcementes(if existing) to users.
    for person in lista_disim:
        for element in messaggi[::-1]:
            try:
                bot.sendMessage(person, utils.text_cleanup(element), parse_mode='HTML', disable_web_page_preview=True)
            except:
                temp.append(person)
                break
    if temp != []:
        for element in temp:
            lista_disim.remove(element)
        utils.save_list(lista_disim, 1)
    dictionary = {}
    lista_annunci = []
    news2 = utils.get_news(disim, 2).find_all('div', 'post_item_list')
    #Updating data structures in case on new announcementes.
    for element in news+news2:
        lista_annunci.append(element.a['href'])
    for i, element in enumerate(news+news2):
        dictionary[lista_annunci[i]] = element.find('p', 'post_description')
