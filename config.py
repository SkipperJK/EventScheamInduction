# MongoDB
MONGODB_HOST = "10.176.24.41"
MONGODB_PORT = 27017
MONGODB_DATABASE_NAME = "Sina"
MONGODB_ARTICLE_COLLECTION = "article20191121_sim"
BULK_SIZE = 2000


# ElasticSearch
ES_HOSTS = ["10.176.24.53:9200"]  #  "10.176.24.56:9200", "10.176.24.57:9200"
ES_HOST = "10.176.24.53"
ES_PORT = 9200
ES_INDEX = "sina_article_20191121"
ES_FIELD_MAPPING = {
    "time": "time",
    "title": "title",
    "content": "content"
}


# pytlp
MODEL_DIR = ''
USER_DICT_DIR = ''