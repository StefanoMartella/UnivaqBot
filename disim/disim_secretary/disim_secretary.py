#!/usr/bin/env python
# -*- coding: utf-8 -*-

def secretary(bot, update):

    secretary_message = ('La segreteria studenti  è situata nel <b>blocco 11/E</b> al 1° piano (a lato dell\'edificio di Medicina), '
                         'i recapiti telefonici sono i seguenti:\n\n\t<i>'
                         '0862433674 - 0862433355</i>.\n\n'
                         'La segreteria è anche contattabile al seguente indirizzo e-mail:\n\n\t<i>'
                         'sestusci@strutture.univaq.it</i>\n\n'
                         'La fascia oraria per i contatti telefonici e tramite posta elettronica è:\n\n'
                         '<b>Lunedì - Mercoledì - Venerdì</b>:\n\n\t<i>'
                         '9:00 - 10:00</i>\n\n<b>Martedì - Giovedì</b>:\n\n\t<i>10:00 - 12:00</i>\n\n'
                         'Gli orari di apertura agli studenti sono i seguenti:\n\n'
                         '<b>Lunedì - Mercoledì - Venerdì</b>:\n\n\t<i>10:00 - 13:00</i>\n\n<b>Martedì - Giovedì</b>:\n\n\t<i>14:30 - 16:00</i>\n\n'
                         'Link alla <a href=\'https://segreteriavirtuale.univaq.it/Home.do\'>segreteria virtuale.</a>')

    bot.sendMessage(update.message.chat_id, secretary_message, disable_web_page_preview=True, parse_mode='HTML')
