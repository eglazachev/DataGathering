from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['test_database']
collection = db.test_collection_test
search_from = float(input("type the salary you want (ex. 10000): "))
for vac in collection.find({"$or": [{"salary_min": {"$gte": search_from}}, {"salary_max": {"$gte": search_from}}]}):
    print(vac)

