from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Researchers']
coll = db['Test']

coll.insert_one({
    "first_name": "Shevinu",
    "last_name": "Nawalage",
    "email": "shevinu2002@gmail.com",
})