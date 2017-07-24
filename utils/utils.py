#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urllib2
from bs4          import BeautifulSoup

#The following three functions are used to load and store users telegram_id.

def get_list(numero):
    with open('/home/stefano/Desktop/UnivaqBot/Users/lista{}.txt'.format(numero), 'r') as f:
        lista = [int(line.rstrip('\n')) for line in f]
    f.close()
    return lista

def save_list(lista, numero):
    with open('/home/stefano/Desktop/UnivaqBot/Users/lista{}.txt'.format(numero), 'w') as f:
        for s in lista:
            f.write('{}'.format(s) + '\n')
        f.close()

def append_in_list(chat_id, numero):
    with open('/home/stefano/Desktop/UnivaqBot/Users/lista{}.txt'.format(numero), 'a') as f:
        f.write('{}'.format(chat_id) + '\n')
        f.close()

#The following function returns soup from giving page usefull to scrape informations thanks to BeautifulSoup.
#In case of no internet connection it tries over and over each fifteen seconds.

def get_news(page, entrant=1):
    while True:
        try:
            web_page = urllib2.urlopen(page.format(entrant))
            soup = BeautifulSoup(web_page, 'lxml')
            return soup
        except:
            time.sleep(15)

#The following function is used to clean the output of /evidenza and /ultimissime commands.

def text_cleanup(text):
    return text.encode('ascii', 'xmlcharrefreplace').replace('&#283;', 'ì').replace('&#146;', '\'').replace('&#341;', 'à').replace('&#150;', '-').replace('&#233;', 'è')
    
