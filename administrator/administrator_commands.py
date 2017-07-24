#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import utils

#The following two commands can be used only by bot administrator(176765549).

def send(bot, update, args):
    #This command can be used just by administrator(176765549).
    #This function can be uset to send a message to a single bot user by knowing his telegram_id thanks to feedback function.
    #Sintax: /send telegram_id message.

    if update.message.chat_id == 176765549:
        if len(args) <= 1:
            return
        text = ''
        for element in args[1::]:
            text += element + ' '
        try:
            bot.sendMessage(args[0], text, parse_mode='HTML')
        except:
            bot.sendMessage(176765549, 'Invio messaggio non riuscito!')

def notify(bot, update, args):
    #This command can be used just by administrator(176765549).
    #This function can be used to notify informations like bot's updates to each user.
    #Sintax: /notify list_num message.

    try:
        index = int(args[0])
    except:
        bot.sendMessage(176765549, 'Invio messaggio non riuscito, devi scegliere a quale lista inviare la notifica!')
        return
    try:
        lista_users = utils.get_list(index)
    except:
        bot.sendMessage(176765549, 'Devi scegliere un numero tra 1 e 3:\n\n 1 = disim,\n 2 = univaq,\n 3 = utenti(tutti).')
        return
    temp = []
    if update.message.chat_id == 176765549:
        for element in lista_users:
            try:
                bot.sendMessage(element, update.message.text.replace("/notify {}".format(index), ''), parse_mode='HTML', disable_web_page_preview=True)
            except:
                temp.append(element)
        if temp != []:
            for element in temp:
                lista_users.remove(element)
            utils.save_list(lista_users, index)

def feedback(bot, update):

    user_feedback_and_informations = ('<b>' + update.message.text + '</b>\n\n <i>{} {}, {}</i>'.format(update.message.from_user.first_name, update.message.from_user.last_name, update.message.chat_id)).replace('/feedback ', '')

    bot.sendMessage(176765549, user_feedback_and_informations, parse_mode='HTML')
    bot.sendMessage(update.message.chat_id, 'Il feedback è stato inviato con successo, grazie per la collaborazione!')
