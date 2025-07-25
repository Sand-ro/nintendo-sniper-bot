import requests
from bs4 import BeautifulSoup
from telegram import Bot
import re
import time
from fake_useragent import UserAgent

TOKEN = '8407177511:AAEyqTkoXa9IfKUwyRVm_4lW-yVzR75eho0'
CHAT_ID = '6562322029'
PREZZO_MAX = 55
INTERVALLO_MINUTI = 3
ua = UserAgent()
bot = Bot(token=TOKEN)

def invia_notifica(lista):
    for msg in lista:
        bot.send_message(chat_id=CHAT_ID, text=msg)

def cerca_sito(url, parser_selection, label):
    try:
        r = requests.get(url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for el in soup.select(parser_selection['item']):
            title = el.select_one(parser_selection['title']).text.lower()
            price = int(re.search(r'(\d{1,3})', el.select_one(parser_selection['price']).text).group(1))
            link = parser_selection['prefix'] + el.select_one(parser_selection['link'])['href']
            if price <= PREZZO_MAX:
                results.append(f'{label}:\n{title}\n💶 {price}€\n🔗 {link}')
        return results
    except:
        return []

def cerca_all():
    return (
        cerca_sito('https://www.subito.it/annunci-italia/vendita/usato/?q=nintendo', {'item':'.ListingCard__Wrapper-sc-1mqc78n-0','title':'.','price':'.','link':'a','prefix':'https://www.subito.it'}, 'Subito')
        + cerca_sito('https://www.ebay.it/sch/i.html?_nkw=nintendo+console&_sop=10&_udhi=40', {'item':'li.s-item','title':'h3.s-item_title','price':'.s-itemprice','link':'a.s-item_link','prefix':''}, 'eBay')
        + cerca_sito('https://www.vinted.it/catalog?search_text=nintendo+console', {'item':'div.feed-grid_item','title':'div.titletext','price':'div.item-box_title--primary','link':'a','prefix':'https://www.vinted.it'}, 'Vinted')
    )

while True:
    ris = cerca_all()
    if ris:
        invia_notifica(ris)
    time.sleep(INTERVALLO_MINUTI * 60)
