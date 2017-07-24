#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Unofficial Univaq's bot created by Stefano Martella.
import os
import time
import urllib2
import telegram
from telegram.ext            import Updater, CommandHandler
from bs4                     import BeautifulSoup
from utils                   import utils
from disim.disim_news        import disim_news
from disim.disim_prof        import disim_prof
from disim.disim_secretary   import disim_secretary
from administrator           import administrator_commands
from univaq.univaq_general   import univaq_general
from univaq.univaq_news      import univaq_news

def start(bot, update):
    lista_users = utils.get_list(3)

    start_message = ('Ciao {}, sono il bot dell\'Univaq,'
                     'per vedere la lista dei comandi clicca su /help.'.format(update.message.from_user.first_name))

    bot.sendMessage(update.message.chat_id, start_message)
    if update.message.chat_id not in lista_users:
        utils.append_in_list(update.message.chat_id, 3)

def help(bot, update):

    help_message = ( 'Lista dei comandi:\n\n'
                     '/help - Mostra la lista dei comandi.\n'
                     '/disim - Mostra le ultime 5 news del Disim.\n'
                     '/disim num - Mostra le ultime \'num\' news del Disim, max 15!\n'
                     '/disimon - Abilita le notifiche per il Disim.\n'
                     '/disimoff - Disattiva le notifiche per il Disim.\n'
                     '/evidenza - Mostra le ultime 5 news della sezione \'In Evidenza\' (Univaq).\n'
                     '/ultimissime - Mostra le ultime 5 news della sezione \'Ultimissime\' (Univaq).\n'
                     '/univaqon - Abilita le notifiche per l\'Univaq.\n'
                     '/univaqoff - Disattiva le notifiche per l\'Univaq.\n'
                     '/prof - Visualizza la lista dei professori del Disim.\n'
                     '/prof cognome - Info su un professore.\n'
                     '/segreteria - Orari, info e link alla segreteria virtuale.\n'
                     '/mensa - Orari e info sulla mensa.\n'
                     '/adsu - Orari, info e link al sito dell\'adsu.\n'
                     '/feedback consiglio - Lascia un commento o un consiglio per migliorare il bot.\n\n'
                     '<i>Bot dedicato agli studenti dell\'Univaq.</i>')

    bot.sendMessage(update.message.chat_id, help_message, parse_mode='HTML')

def main():
    token = '304755425:AAEzMUEs7i4A38Xn2u_RCMj6XmBc5X24Hxg'
    updater = Updater(token)
    dp = updater.dispatcher

    #Filling data structures.
    disim_news.preparing_disim()
    univaq_news.preparing_univaq()
    disim_prof.preparing_prof()
    
    updater.job_queue.run_repeating(disim_news.check_disim_news, 150)
    updater.job_queue.run_repeating(univaq_news.check_univaq_news, 150)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("disim", disim_news.show_disim_news, pass_args=True))
    dp.add_handler(CommandHandler("disimon", disim_news.disimon))
    dp.add_handler(CommandHandler("disimoff", disim_news.disimoff))
    dp.add_handler(CommandHandler("evidenza", univaq_news.evidenza))
    dp.add_handler(CommandHandler("ultimissime", univaq_news.ultimissime))
    dp.add_handler(CommandHandler("univaqon", univaq_news.univaqon))
    dp.add_handler(CommandHandler("univaqoff", univaq_news.univaqoff))
    dp.add_handler(CommandHandler("prof", disim_prof.prof))
    dp.add_handler(CommandHandler("segreteria", disim_secretary.secretary))
    dp.add_handler(CommandHandler("mensa", univaq_general.canteen))
    dp.add_handler(CommandHandler("adsu", univaq_general.adsu))
    dp.add_handler(CommandHandler("feedback", administrator_commands.feedback))
    dp.add_handler(CommandHandler("send", administrator_commands.send, pass_args=True))
    dp.add_handler(CommandHandler("notify", administrator_commands.notify, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
