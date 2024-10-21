from pymongo import MongoClient
from configs import MONGO_CONN_STR, MONGO_DB

db = MongoClient(MONGO_CONN_STR)[MONGO_DB]
