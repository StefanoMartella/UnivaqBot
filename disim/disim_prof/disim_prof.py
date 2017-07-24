#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from utils import utils

prefix_disim = 'http://www.disim.univaq.it/main/{}'
people = 'http://www.disim.univaq.it/main/people.php'
elenco_prof = []

#Filling data structures.

def preparing_prof():
    global elenco_prof

    elenco_prof = utils.get_news(people).find_all('li')[44:165]

#This function according to the given 'args' prints or the whole list of prof(if no 'args')
# either prof's informations (if 'args' is equal to a existing prof's name).

def prof(bot, update):
    if update.message.text == '/prof':
        categories = utils.get_news(people).find_all('div', 'acc_item')[0:4]
        text = ''
        for element in categories:
            text += '\n<b>' + element.find('span', 'acc_heading').get_text() + '</b>:\n\n'
            index = element.find_all('strong')
            for i in range(0, len(index)):
                text += '<i>' + element.find_all('strong')[i].get_text() + '</i>\n'
        bot.sendMessage(update.message.chat_id, text, parse_mode='HTML')
    else:
        surname = update.message.text.lower().replace('/prof ', '')
        if len(surname) < 4:
            bot.sendMessage(update.message.chat_id, 'Non trovo nessun docente con quel cognome!')
            return
        global elenco_prof
        entry = ''
        for element in elenco_prof:
            if surname in element.strong.string.lower():
                entry = element.a['href']
                soup = utils.get_news(prefix_disim, entry)
                prof_informations = ('<b>' + soup.find('h1').string + '</b>\n\n<b>'
                                     'Stanza:</b>\n<i>' + ('Non disponibile' if (soup.find('div', 'icon_loc').get_text() == ' , Room ') else soup.find('div', 'icon_loc').get_text()) + '\n\n</i><b>' +
                                     'Email:</b>\n\t' + (soup.find('div', 'icon_mail').get_text() or '<i>Non disponibile</i>') + '\n\n<b>' +
                                     'Telefono:</b>\n\t' + (soup.find('div', 'icon_phone').get_text() or '<i>Non disponibile</i>') + '\n\n<b>' +
                                     'Curriculum vitae:\n\t</b>' + ('<a href=\'' + soup.find('div', 'icon_cv').a['href'] + '\'>' + ((soup.find('div', 'icon_cv').get_text()) + '</a>') or '<i>Non disponibile</i>') + '\n\n<b>' +
                                     'Corsi:\n\t</b>')
                courses = soup.find_all('div', 'ten columns')[::-1][0:1]
                if len(courses) == 1:
                    for course in courses[0].find_all('a'):
                        prof_informations += '\t- <a href=\'' + course['href'] + '\'>' + course.string + '</a>' + '\n\n'
                else:
                    prof_informations += '<i>Non disponibile</i>'
                bot.sendMessage(update.message.chat_id, prof_informations, parse_mode='HTML', disable_web_page_preview=True)
                return
        bot.sendMessage(update.message.chat_id, 'Non trovo nessun docente con quel cognome!')
