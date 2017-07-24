#!/usr/bin/env python
# -*- coding: utf-8 -*-

def canteen(bot, update):

    canteen_message = ('Gli orari della mensa di <b>Coppito</b> e di <b>Campomizzi</b> sono:\n\n'
                       '<b>Lunedì - Venerdì:</b>\n\n\t<i>12:30 - 15:00</i>\n\n'
                       'Per usufruire del servizio mensa è necessaria la <b>tessera</b> ritirabile presso gli uffici /adsu di Campomizzi. '
                       'La tessera ha durata di un <b>anno solare</b>, quindi il 31 Dicembre di ogni anno essa scade indipendentemente dalla data di rilascio.')

    bot.sendMessage(update.message.chat_id, canteen_message, parse_mode='HTML')

def adsu(bot, update):

    adsu_message = ('<b>Azienda per il diritto agli studi universitari.</b>\n\n<b>'
                    'Sede legale:</b>\n\n<i>'
                    'Via XX Settembre, 46/52\n67100 L\'Aquila\n\n</i><b>'
                    'Sede operativa:</b>\n\n<i>'
                    'Ex Caserma Campomizzi,\nLocalità S.Antonio - Casermette,\nPalazzina \"D\" - 67100 L\'Aquila</i>\n\n<b>'
                    'Telefono:\n\n</b><i>086232701</i>\n\n'
                    'Gli <b>Orari</b> degli uffici adsu sono i seguenti:\n\n<b>'
                    'Luendì:</b>\n\n\t<i>11:30 - 13:30</i>\n<b>Esclusivamente per il ritiro tessere mensa.</b>\n\n<b>'
                    'Martedì e Giovedì:</b>\n\n\t<i>15:00 - 17:00</i>\n\n'
                    'Link al sito dell\' <a href=\'http://www.adsuaq.org/\'>adsu</a>.')

    bot.sendMessage(update.message.chat_id, adsu_message,parse_mode='HTML')
