import json
import unittest
import logging
import jieba
from config import *
from elasticsearch import Elasticsearch
from ESIServer.model.ArticleES import ArticleES
from ESIServer.model.ArticleES import customAritcleESDecoder

es = Elasticsearch(ES_HOSTS)
debug_logger = logging.getLogger('debug')


def search_articles(topic ='', size=10000):
    """
    TODO 有三种，title和content
    :param topic:
    :param size:
    :return:
    """

    keywords = []
    for word in jieba.cut(topic):
        keywords.append(word)

    action = {
        "size":size,
        "query":{
            "bool": {
                "must":[
                # "should": [
                #     {
                #       # "match": {
                #       "match_phrase":{
                #         "title": topic
                #       }
                #     },
                    # {
                    #   "match": {
                    #     "content": keywords
                    #   }
                    # }
                ]
            }
        }
    }

    for word in keywords:
        action["query"]["bool"]["must"].append({'match': {"title": word}})
    print(action)


    response = es.search(body=action, index=ES_INDEX) # ES返回的是dict类型，
    articles = []
    for articleDict in response["hits"]["hits"]:
        # articles.append(ArticleES(**articleDict['_source']))
        score = articleDict['_score']
        source = articleDict['_source']
        source['score'] = score
        articles.append(ArticleES(**source))
        # articles.append(ArticleES(source['title'], source['content'], source['time'], score))
    # find_point([art.score for art in articles])
    return articles



def find_point(scores):
    debug_logger.debug(scores)
    import matplotlib.pyplot as plt
    plot_objs = plt.subplots(nrows=3, ncols=1, figsize=(12, 6))
    print(plot_objs)
    fig, (ax1, ax2, ax3) = plot_objs
    ax1.plot(scores)
    slopes = []
    diffs = []
    for i in range(0, len(scores)-1):
        slopes.append(scores[i+1]-scores[i])
        diffs.append(scores[i+1]-scores[i])
    debug_logger.debug(slopes)
    debug_logger.debug(diffs)
    ax2.plot(slopes)
    ax3.plot(diffs)
    plt.show()

class TESTES(unittest.TestCase):

    def test_search(self):
        topic = '中国'
        topic = '吴昕金牛座男友'
        topic = "马航MH370"
        # topic = '奥斯卡提名'
        articles = search_articles(topic, 200)
        scores = []
        for idx, article in enumerate(articles):
            debug_logger.debug("idx: {},id: {} score: {} title: {}".format(idx, article.id, article.score, article.title))
            scores.append(article.score)
            # print(article.__dict__)
            # debug_logger.debug(article.__dict__)


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