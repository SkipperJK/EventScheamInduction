import logging
import numpy as np
from unittest import TestCase
from collections import OrderedDict
from sknetwork.ranking import PageRank
from ESIServer.model.Triple import UniqueTriple
from ESIServer.model.TripleBigram import TripleBigram
from ESIServer.component.open_relation_extraction.extract import extract
root_logger = logging.getLogger('root')
debug_logger = logging.getLogger('debug')
trace_logger = logging.getLogger('trace')


class TripleGraph:
    """
    构建Triple的共现矩阵，计算每对元组之间的权重
    """

    def __init__(self, triples, k=10, num_seeds=2, topN=10):
        """
        TODO: 重构为fit方法的形式
        输入多个doc抽取得到的triples构建TripleGraph
        :param triples: [[[],[],...], [[],...]]] 三维list： document，sentence，triple
        """
        self.triples = triples
        self.k = k
        trace_logger.info("Get unique triples...")
        self.triple_count_dict = self.get_unique_triples()
        trace_logger.info("Calculate co-occurrence count...")
        self.co_occurrence_table = self.calculate_co_occurrence_table()
        self.triple_condition_prob = self.calculate_conditional_probability()
        self.edge_weight = self.calculate_undirected_edge_weight()
        self.triples_of_events = []
        seeds = self.top_n_nodes(self.edge_weight, num_seeds=num_seeds)
        for seed in seeds:
            self.triples_of_events.append(self.get_triples_of_event(seed, topN))


    def get_unique_triples(self):
        """将每个元组映射到唯一的标识符，并列出元组计数
        TODO; 过滤掉低频的triple, 例如 >=3
        :return:
        """
        triple_count_dict = OrderedDict()
        for doc in self.triples:
            for sent in doc:
                for triple in sent:
                    unique_triple = UniqueTriple(triple.arg1, triple.rel, triple.arg2)
                    triple_count_dict[unique_triple] = triple_count_dict.get(unique_triple, 0) + 1
        self.unique_triples = []
        self.id2triple = {}
        self.triple2id = {}
        for idx, triple in enumerate(triple_count_dict.keys()):
            triple.id = idx
            self.unique_triples.append(triple)
            self.id2triple[idx] = triple
            self.triple2id[triple] = idx
        return triple_count_dict


    def calculate_co_occurrence_table(self, k=10):
        """计算元组文档中以及文档之间的共现计数
        四种平等约束：E11，E12，E21，E22
        :param k: 两个元组之间最大距离 有向的向后距离小于k的元组
        :return:
        """
        self.k = k
        co_occurrence_table = []
        bigram_count_dict = OrderedDict()
        for doc in self.triples:
            triples_doc = [triple for triple_sent in doc for triple in triple_sent]
            for idx1 in range(len(triples_doc)):
                t1 = triples_doc[idx1]
                ut1 = UniqueTriple(t1.arg1, t1.rel, t1.arg2)
                for idx2 in range(idx1+1, len(triples_doc)):
                    t2 = triples_doc[idx2]
                    if 0 < t2.num - t1.num <= self.k:
                        ut2 = UniqueTriple(t2.arg1, t2.rel, t2.arg2)
                        triple_bigram = TripleBigram(self.triple2id[ut1], self.triple2id[ut2], t2.num-t1.num, 1)
                        bigram_count_dict[triple_bigram] = bigram_count_dict.get(triple_bigram, 0) + 1
                    else:
                        continue

        debug_logger.debug("Co-occurrence table:")
        for triple_bigram, count in bigram_count_dict.items():
            triple_bigram.count = count
            co_occurrence_table.append(triple_bigram)
            debug_logger.debug(triple_bigram.to_string())
        return co_occurrence_table


    def calculate_conditional_probability(self, sigma=0.05, alpha=0.5):
        """
        计算triple bi-gram的条件概率
        P_k(T'|T)： T之后距离为k的T'的条件概率     (#(T,T',k)+\sigma) / (\sum_{T'' \in V} #(T,T'',k) + \sigma |V|
        P(T'|T) : P_k的所有k下的加权
        :return:
        """
        trace_logger.info("Calculating conditional probability...")
        num_uts = len(self.unique_triples)
        t_k_count = np.zeros((num_uts, self.k))  # \sum_{T'' \in V} #(T,T'',k)
        t1_t2_k_prob = np.zeros((num_uts, num_uts, self.k))  # P_k(t2|t1)  t2在t1条件下且距离为k的条件概率
        triple_condition_prob = np.zeros((num_uts, num_uts))  # [T][T'] -> P(T'|T)
        debug_logger.debug(
            "Init t_k_count: {} \n Init t1_t2_k_prob: {} \n Init triple_condition_prob: {}".format(
                t_k_count, t1_t2_k_prob, triple_condition_prob)
        )

        for triple_bigram in self.co_occurrence_table:
            id1 = triple_bigram.id_t1
            dist = triple_bigram.dist
            t_k_count[id1][dist - 1] += triple_bigram.count  # 统计t后距离为k的所有triple的个数（作为条件概率的分母）
        debug_logger.debug(
            "t_k_count: {}".format(t_k_count)
        )

        for triple_bigram in self.co_occurrence_table:
            id1 = triple_bigram.id_t1
            id2 = triple_bigram.id_t2
            dist = triple_bigram.dist
            t1_t2_k_prob[id1][id2][dist - 1] = (triple_bigram.count + sigma) / (
                        t_k_count[id1][dist - 1] + num_uts * sigma)
        indices_sat = np.where(t1_t2_k_prob == 0)  # 平滑处理：共现为0的
        for id1, id2, k in zip(indices_sat[0], indices_sat[1], indices_sat[2]):
            t1_t2_k_prob[id1][id2][k] = sigma / (sum(t1_t2_k_prob[id1, :, k]) + num_uts * sigma)
        debug_logger.debug(
            "t1_t2_k_prob: {}".format(t1_t2_k_prob)
        )

        divided = sum([np.power(alpha, i) for i in range(1, self.k + 1)])
        for id1 in range(0, num_uts):
            for id2 in range(0, num_uts):
                tmp = sum([np.power(alpha, i) * t1_t2_k_prob[id1][id2][i - 1] for i in range(1, self.k + 1)])
                triple_condition_prob[id1][id2] = tmp / divided
        debug_logger.debug(
            "triple_condition_prob: {}".format(triple_condition_prob)
        )

        return triple_condition_prob


    def calculate_undirected_edge_weight(self):
        """
        计算无向边的权重
        SCP(T,T') = P(T'|T) P(T|T')
        :return:
        """
        trace_logger.info("Calculating edge weight...")
        num_uts = len(self.unique_triples)
        edge_weight = np.zeros((num_uts, num_uts))
        debug_logger.debug(
            "Init edge_weight: {}".format(edge_weight)
        )
        for i in range(len(self.unique_triples)):
            for j in range(i, len(self.unique_triples)):
                edge_weight[i][j] = self.triple_condition_prob[i][j]*self.triple_condition_prob[j][i]
                edge_weight[j][i] = edge_weight[i][j]
        debug_logger.debug(
            "edge_weight: {}".format(edge_weight)
        )

        return edge_weight


    def top_n_nodes(self, edge_weight, num_seeds=3):
        """
        选出具有代表行的triple, 将每个点相连的边按照权重排序，只比较Top25条边的和
        :param edge_weight: ndarray
        :param n:  int
        :return: list
        """
        # vertex_weight.sort(axis=1)
        vertex_weight = edge_weight.sum(axis=1)
        idx_sorted = np.argsort(-vertex_weight)  # 降序 == 取负升序

        return idx_sorted.tolist()[:num_seeds]


    def subgraph(self, seed, hops=2):
        """
        对种子点构建两跳之内的子图 （由于平滑处理之后的不好判断哪些点之间没有边，因此可以根据非泛化之间来找两跳之内的子图）
        :return:
        """
        vertices_subgraph = []
        for idx, weight in enumerate(self.edge_weight[seed]):
            if weight != 0:
                vertices_subgraph.append(idx)
        vertices_subgraph = set(vertices_subgraph)
        vertices_subgraph = list(vertices_subgraph)
        for vertex in vertices_subgraph:
            for idx, weight in enumerate(self.edge_weight[vertex]):
                if weight != 0:
                    vertices_subgraph.append(idx)
        vertices_subgraph = set(vertices_subgraph)
        edge_weigth_subgraph = np.zeros((len(vertices_subgraph), len(vertices_subgraph)))
        idx2vertex = {i: vectex for i, vectex in enumerate(vertices_subgraph)}
        for idx1 in range(len(vertices_subgraph)):
            for idx2 in range(len(vertices_subgraph)):
                edge_weigth_subgraph[idx1][idx2] = self.edge_weight[idx2vertex[idx1]][idx2vertex[idx2]]

        return vertices_subgraph, edge_weigth_subgraph


    def get_triples_of_event(self, seed_vertex, topN=10):
        """
        先得到种子点，然后执行personal PageRank得到与种子点相关的triples
        :return:
        """
        triples_of_event = []
        topN = topN if topN < len(self.unique_triples) else len(self.unique_triples)
        pagerank = PageRank()
        scores = pagerank.fit_transform(self.edge_weight, {seed_vertex: 1})  # 对每个种子点运行Personal PageRank
        idx_sorted = np.argsort(-scores)
        for idx in idx_sorted[:topN]:
            triples_of_event.append(self.unique_triples[idx])

        debug_logger.debug("seed vertex: {}".format(seed_vertex))
        for idx in idx_sorted:
            debug_logger.debug("weight: {}, triple: {}".format(scores[idx], self.unique_triples[idx].to_string()))

        return triples_of_event



class TestTripleGraph(TestCase):

    def test_unique_triples(self):
        origin_sentences = [
            "习近平主席访问奥巴马总统先生",
            "习近平主席视察厦门，李克强访问香港",
            "李克强总理今天来我家了，我赶紧往家里跑。",
            "习近平主席访问奥巴马总统先生",
            "浮士德与魔鬼达成协议。",
            "巴拿马在2007年与中国建立关系。",
            "德国总统高克。",
            "高克访问中国。",
            "习近平在上海视察。",
            "习近平对埃及进行国事访问。",
            "奥巴马毕业于哈佛大学。",
            "习近平主席和李克强总理接见普京。",
            "习近平访问了美国和英国。",
            "高克访问中国，并在同济大学发表演讲。",
            "李明出生于1999年。"
        ]

        triples = extract(origin_sentences)
        triple_graph = TripleGraph([triples])
        idx = 0
        for triple, count in triple_graph.triple_count_dict.items():
            debug_logger.debug('{:d} - {:s}: {:d}'.format(idx, str(triple), count))
            idx += 1

        debug_logger.debug('Test id2triple: {:s}'.format(str(triple_graph.id2triple[10])))
        debug_logger.debug('Test triple2id: {:d}'.format(triple_graph.triple2id[triple_graph.unique_triples[2]]))




