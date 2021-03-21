from pymongo import MongoClient
import csv


client = MongoClient('localhost', 27017)
db = client['test_database']
collection = db.test_collection_test
vacancies = []
with open('out_old.csv', newline='', encoding="utf8") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    head = next(reader)
    keys = []
    for titles in head:
        keys.append(titles)
    for row in reader:
        vacancy_item = {}
        for (key, val) in zip(keys, row):
            try:
                val = float(val)
            except:
                pass
            vacancy_item[key] = val
        vacancies.append(vacancy_item)
