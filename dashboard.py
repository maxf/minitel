from emunitel import Minitel
import time
import requests
from datetime import datetime


minitel = Minitel.Minitel()


def send_to_minitel(news):
    minitel.efface()



    minitel.position(1,2)
    minitel.taille(2,2)
    minitel.envoyer(f"3615 Hacker News")

    date_now = datetime.now().strftime("%d %b")
    time_now = datetime.now().strftime("%H:%M")
    minitel.position(35,1)
    minitel.envoyer(date_now)
    minitel.position(36,2)
    minitel.envoyer(time_now)


    for line in range(0, 5):
        minitel.position(1,3*line+5)
        minitel.envoyer(f"* {news[line]}")




while True:

    r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    j = r.json()[0:5]
    news = []

    for news_id in j:
        n = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{news_id}.json')
        n2 = n.json()
        news.append(n2['title'])

    send_to_minitel(news)

    time.sleep(10)
