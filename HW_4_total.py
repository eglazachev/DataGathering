import requests
from lxml import html
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['news']
collection = db.news
collection.drop()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
url = "https://lenta.ru"
xpath_string = '//div[contains(@class, "span4")]//div[contains(@class, "item") and not(contains(@class, "tabloid"))]//a[not(contains(@class, "rubric" )) and not(contains(@class, "favorite"))]'

r = requests.get(url, headers)
s = r.text
doc = html.fromstring(s)
elems = doc.xpath(xpath_string)
all_news = []
for elem in elems:
    news = {}
    news['source'] = url
    title = elem.xpath('./text()')
    time = elem.xpath('./time/@datetime')
    link = elem.xpath('./@href')
    if len(time) != 0:
        news['time'] = time[0]
    if len(title) != 0:
        title = title[0].replace(u'\xa0', u' ')
        news['title'] = title
        if len(link) != 0:
            news['link'] = url + link[0]
            all_news.append(news)

url = "https://yandex.ru/news/"
xpath_string = '//article'

r = requests.get(url, headers)
s = r.text
doc = html.fromstring(s)
elems = doc.xpath(xpath_string)
for elem in elems:
    news = {}
    title = elem.xpath('.//a/h2/text()')
    link = elem.xpath('.//a/@href')
    time = elem.xpath('.//span[contains(@class, "__time")]/text()')
    if len(title) != 0:
        title = title[0].replace(u'\xa0', u' ')
        news['title'] = title
        news['link'] = link[0]
        news['time'] = time[0]
        news['source'] = url
    all_news.append(news)

url = "https://news.mail.ru"
xpath_string = '//div[contains(@class, "daynews__item")]'

r = requests.get(url, headers)
s = r.text
doc = html.fromstring(s)
elems = doc.xpath(xpath_string)
for item in elems:
    title = item.xpath('//span[contains(@class,"__title")]/text()')
    link = item.xpath('//a/@href')
    time = ''
if len(title) != 0:
    for i in range(0, len(elems)):
        news = {}
        news['title'] = title[i].replace(u'\xa0', u' ')
        news['link'] = link[i]
        news['time'] = time
        news['source'] = url
        all_news.append(news)
xpath_string = '//div[@data-module="TrackBlocks"]//li[@class="list__item"]/a'
elems = doc.xpath(xpath_string)
for item in elems:
    title = item.xpath('./text()')
    link = item.xpath('./@href')
    if len(title) != 0:
        news = {}
        news['title'] = title[0].replace(u'\xa0', u' ')
        news['link'] = link[0]
        news['time'] = time
        news['source'] = url
        all_news.append(news)


collection.insert_many(all_news)
