import logging
# import config   # config文件中进行 fileConfig加载配置文件
from ESIServer.component.triple_cluster.TripleGraph import TripleGraph
from ESIServer.component.elasticsearch import search
from ESIServer.component.open_relation_extraction.extract import extract
from ESIServer.model.Triple import Triple
root_logger = logging.getLogger('root')
debug_logger = logging.getLogger('debug')
trace_logger = logging.getLogger('trace')
debug_logger.setLevel(logging.INFO)
# trace_logger.setLevel(logging.WARNING)
if 'DEBUG' not in locals().keys():
    DEBUG = True if debug_logger.level == logging.DEBUG else False


if __name__ == '__main__':

    topic = "赵丽颖生子"
    topic = "马航MH370"  # 大概有40篇相关性比较强的文章
    # topic = "出轨"
    articles = search.search_articles(topic,40)

    all_triples = []
    for idx_art, article in enumerate(articles):
        trace_logger.info('{}:{}'.format(idx_art, article.title))
        triples = extract(article.sentence_of_content, idx_art)
        all_triples.append(triples)
        if DEBUG:
            for triples_of_sent in triples:
                for triple in triples_of_sent:
                    debug_logger.debug(triple.to_string())

    triple_graph = TripleGraph(all_triples)
    t = triple_graph.get_unique_triples()
    idx = 0
    for triple, count in t.items():
        root_logger.info('{:d} - {:s}: {:d}'.format(idx, str(triple), count))
        idx += 1

    for num,triples in enumerate(triple_graph.triples_of_events):
        root_logger.info('Event ID: {}'.format(num))
        for idx, triple in enumerate(triples):
            root_logger.info('Index: {}, Triple: {}'.format(idx, triple))



# 1 标记把原文替换, 找几篇相似文章，模版替换之后看效果
# 2 计算权重，跑pagerank
# jia hao yang 学姐要论文



'''
1。 文章相关性分析   es召回率的score


'''