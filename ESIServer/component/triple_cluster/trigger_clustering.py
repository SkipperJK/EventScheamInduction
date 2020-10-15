import sys
sys.path.append('../../')
import json
import numpy as np
import math
import pickle
from ESIServer.model.Triple import Triple
from pymongo import MongoClient
from sklearn.cluster import AgglomerativeClustering

# corsor.skip().limit()
'''语料问题：
    1. 包含很多日文     -》 如何过滤日文
'''

'''
问题一： 就是这里的主谓关系可能主语大多数时名词，但是动宾关系的话宾语可能时动词，这怎么处理
    1. 只提取主语和宾语都是名词的三元组   -》 目前使用这种方法
    2. 其他处理方法
    
问题二： 提取的主语和宾语有可能时代词，就是需要使用代指消解。
    1. 找中文相关方面的实现。
    
问题三： 三元组是否要完整的三元组
    1. 完整三元组，有主语和宾语  -》目前使用这种方法
    2. 有主语或者宾语其中至少一个
    3. 两个都没有也可以
'''





'''
Algorithm:
    1. find all trigger along with triple 
    2. construct the trigger vocabulary
    3. calculate C(w1,w2) for all pairs of trigger in the vocab
    4. calculate pmi(w1,w2) for all pairs of trigger in the vocab
没有考虑trigger顺序信息。
'''
doc_triples = []
empty_count = 0
triple_count = 0
trigger_vocab = []
trigger_count_dict = {}  # 统计每个trigger出现了多少次


for i, article in enumerate(corsor):
    if len(article['sentences']) == 1 and article['sentences'][0]['sentence'] == '':
        # print(i)
        empty_count += 1
        continue

    triples = []
    for j, sent in enumerate(article['sentences']):
        for k, word in enumerate(sent['words']):
            '''
            if word is trigger:
                find sub, obj of trgger
                triggers.append(Trigger())
            # consider the empty article result
            version-1: all articles have the sentence filed in mongo even if is empty.
            '''
            if word['postag'][0] != 'v':
                continue
            # print(word['lemma'])
            sub, obj = find_sub_obj(word, sent['words'])
            if sub == None or obj == None:
                continue
            triple = Triple(i, j, word['lemma'], sub['lemma'], obj['lemma'])
            triples.append(triple)
            triple_count += 1

            trigger_count_dict[triple.word] = trigger_count_dict.get(
                triple.word, 0) + 1
            trigger_vocab.append(word['lemma'])
    doc_triples.append(triples)

  #  if i > 40 :
  #      break
    if triple_count > 10000:
        break

# output test the result
# for i, triples in enumerate(doc_triples):
#    print(i, len(triples))
#    for j, triple in enumerate(triples):
#        print(triple)


#triple_count = sum(trigger_count_dict.values())
print("不包含Triple的文章个数:%d, 总共的triple个数:%d" % (empty_count, triple_count))

# triggerPair_weight = {}  # 这种方法占用的空间太大，实际上对于聚类需要的就是每两个trigger之间的相似度
# 因此只需要构建一个二维矩阵，trigger2Ind存储trigger对应的索引，还有id2trigger就是一个list
trigger_vocab = list(set(trigger_vocab))
vocab_size = len(trigger_vocab)
print("tirggers集合中trigger个数: %d" % vocab_size)

trigger2Ind = {}
for idx, trigger in enumerate(trigger_vocab):
    trigger2Ind[trigger] = idx


# 1. initial the triggerPair distance weight to zero
print("初始化距离权重矩阵...")
weight_distance_matrix = np.zeros((vocab_size, vocab_size))
print("权重矩阵的维度：", weight_distance_matrix.shape)


def calculate_distance_weight(weight_distance_matrix, doc_triples):
    '''
    calculate the C(w1,w2) of trigger1 and trigger2
    C(w1, w2): 1-log(g(w1,w2)  # for all trigger pair in same doc of all corpus
        g=1 -> C=1
        g=2 -> C=0.5

    g(w1,w2): represent distance of two triggers in the same doc.
        1: in the same sentence
        2: in neighboring

    :return:  trigger pair weight dict
    '''
    for i, triples in enumerate(doc_triples):
        num = len(triples)
        for i in range(num):
            for j in range(i+1, num):
                g = 1 if triples[i].sent_num == triples[j].sent_num else 2

                idx1, idx2 = trigger2Ind[triples[i].word], trigger2Ind[triples[j].word]
                weight_distance_matrix[idx1][idx2] += 1-math.log(g, 4)
                weight_distance_matrix[idx2][idx1] += 1-math.log(g, 4)
    return weight_distance_matrix


# 2. calc the triggerPair distance weight
print("计算权重矩阵...")
weight_distance_matrix = calculate_distance_weight(weight_distance_matrix, doc_triples)
print('-'*20)


def pmi(weight_distance_matrix, trigger_count_dict):
    '''
    calculate pmi of two triggers
    pmi(w1, w2) = P_dist(w1, w2) / P(w1)P(w2)
        P_dist(w1, w2) =
        P(w1) =
    :return:
    '''

    pmi_matirx = np.zeros((vocab_size, vocab_size))
    trigger_count = sum(trigger_count_dict.values())
    sum_of_weight = np.sum(np.triu(weight_distance_matrix)) # np.triu(d) 上三角矩阵

    for i in range(vocab_size):
        for j in range(vocab_size):
            p_dist = weight_distance_matrix[i][j] / float(sum_of_weight)
            p_t1 = trigger_count_dict[trigger_vocab[i]] / float(trigger_count)
            p_t2 = trigger_count_dict[trigger_vocab[j]] / float(trigger_count)
            pmi_matirx[i][j] = p_dist / p_t1 * p_t2

    return pmi_matirx


# 3. calc triggerPair Weight
pmi_matirx = pmi(weight_distance_matrix, trigger_count_dict)
print(np.max(pmi_matirx))

'''
AgglomerativeClustering()模型的使用：
    输入的时计算好的距离矩阵，因此设定参数 affinity='precomputed',
    类之间的距离计算使用样本的平均距离，因此设定参数linkage='average'
'''
n_clusters = 10
clustering = AgglomerativeClustering(n_clusters=n_clusters, affinity='precomputed', linkage='average') # 样本的平均距离作为簇之间的距离
clustering.fit_predict(pmi_matirx)
print(clustering.labels_)
labels = clustering.labels_

trigger_clust = []
for i in range(n_clusters):
    inds = np.where(labels == i)[0]  # where返回的时tuple的tuple
    triggers = []
    for ind in inds:
        triggers.append(trigger_vocab[ind])
    trigger_clust.append(triggers)
    print("cluster %d, triggers count: %d" % (i, len(inds)))

import json
with open("./trigger_clusters.txt", 'w') as fw:
    for clust in trigger_clust:
        fw.write(' '.join(clust))
        fw.write('\n')
exit(0)


ret = sorted(triggerPair_pmi.items(), key=lambda x: x[1], reverse=True)
print(ret[:2])
with open("pmi.json", 'w') as fw:
    json.dump(ret, fw)

with open('pmi.txt', 'w') as fw:
    fw.write(json.dumps(ret, indent=4, ensure_ascii=False))
    

