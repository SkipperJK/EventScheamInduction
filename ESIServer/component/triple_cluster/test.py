from pymongo import MongoClient
from config import *

conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collet = db[MONGODB_ARTICLE_COLLECTION]

