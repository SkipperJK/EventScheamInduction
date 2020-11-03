import os
import sys
import logging.config

#PROJECT_DIR = sys.path[0] # 执行文件所在路径，并不一定是config.py文件所在路径
#PROJECT_DIR = os.getcwd() # 执行文件所在路径，并不一定是config.py文件所在路径
#PROJECT_DIR = __file__ # 当前文件路径
PROJECT_DIR = os.path.dirname(__file__) # 当前文件目录


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
LTP_MODEL_DIR = os.path.join(PROJECT_DIR, 'ESIServer/data/pretrained_model/LTPModel')
LTP4_MODEL_DIR = os.path.join(PROJECT_DIR, 'ESIServer/data/pretrained_model/LTPModel')
USER_DICT_DIR = os.path.join(PROJECT_DIR, 'ESIServer/data/user_dicts')

LOG_CONFIG_DIR= os.path.join(PROJECT_DIR, 'logging.conf')
# 由于logs路径问题：这里配置logging
logging.config.fileConfig(LOG_CONFIG_DIR)