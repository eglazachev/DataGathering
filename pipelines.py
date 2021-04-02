# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient
MONGO_URL = "localhost:27017"
# MONGO_URL = "localhost:27019"


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client['vacancy']

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            if len(item["salary"]) > 1:
                for el in item["salary"]:
                    if el.find('от') != -1:
                        i = item["salary"].index(el)
                        item["salary_min"] = item["salary"][i + 1].replace(u'\xa0', u'')
                    if el.find('до') != -1:
                        i = item["salary"].index(el)
                        item["salary_max"] = item["salary"][i + 1].replace(u'\xa0', u'')
                        break
                del item["salary"]
            else:
                item["salary"] = item["salary"][0]

        if spider.name == 'sj':
            if len(item["salary"]) > 1:
                if item["salary"][0] == 'от':
                    item["salary_min"] = item["salary"][2].replace(u'\xa0', u'')
                    item["salary_min"] = item["salary_min"].replace('руб.', '')
                if item["salary"][0] == 'до':
                    item["salary_max"] = item["salary"][2].replace(u'\xa0', u'')
                    item["salary_max"] = item["salary_max"].replace('руб.', '')
                if item["salary"][0].find(u'\xa0') != -1:
                    item["salary_min"] = item["salary"][0].replace(u'\xa0', u'')
                    item["salary_max"] = item["salary"][1].replace(u'\xa0', u'')
                del item["salary"]
            else:
                item["salary"] = item["salary"][0]

        collection = self.db[spider.name]
        if collection.find({'link': item['link']}).count() == 0:
            collection.insert_one(item)

        return item
