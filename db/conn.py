from pymongo import MongoClient
import os

print(os.getenv("MONGO_CONN_STR"))
db = MongoClient(os.getenv("MONGO_CONN_STR"))[os.getenv("MONGO_DB")]
