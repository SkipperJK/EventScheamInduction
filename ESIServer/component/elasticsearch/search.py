import json
from config import *
from elasticsearch import Elasticsearch
from core.model.ArticleES import ArticleES
from core.model.ArticleES import customAritcleESDecoder

es = Elasticsearch(ES_HOSTS)


def search_articles(keywords = '', size=10000):
    action = {
        "size":size,
        "query":{
            "bool": {
                "should": [
                    {
                      "match": {
                        "title": keywords
                      }
                    },
                    {
                      "match": {
                        "content": keywords
                      }
                    }
                ]
            }
        }
    }


    response = es.search(body=action, index=ES_INDEX) # ES返回的是dict类型，
    articles = []
    for articleDict in response["hits"]["hits"]:
        articles.append(ArticleES(**articleDict['_source']))
    return articles


if __name__ == '__main__':
    articles = search_articles("中国", 3)
    for article in articles:
        print(article.__dict__)

'''ES return item
{
    '_index': 'sina_article_20191121', 
    '_type': '_doc', 
    '_id': '5f57634b83577eadc453f7c9', 
    '_score': 10.074459, 
    '_source': {
        'time': '2019-10-01 13:50:19', 
        'title': '中国色彩，中国味道，中国红，中国创意。', 
        'content': '中国色彩，中国味道，中国红，中国创意。
    }
}
'''