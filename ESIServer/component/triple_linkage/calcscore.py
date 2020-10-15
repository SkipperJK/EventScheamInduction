import numpy as np




def distance_weight(weight_distance_matrix, doc_triples):
    """Calculate trigger distance weight C(w1,w2) of trigger1 and trigger2

    C(w1, w2): 1-log(g(w1,w2)  # for all trigger pair in same doc of all corpus

        g=1 -> C=1
        g=2 -> C=0.5

    g(w1,w2): represent distance of two triggers in the same doc.

        1: in the same sentence
        2: in neighboring

    :param weight_distance_matrix:
    :param doc_triples:
    :return: trigger pair weight dict
    """
    for i, triples in enumerate(doc_triples):
        num = len(triples)
        for i in range(num):
            for j in range(i+1, num):
                g = 1 if triples[i].sent_num == triples[j].sent_num else 2

                idx1, idx2 = trigger2Ind[triples[i].word], trigger2Ind[triples[j].word]
                weight_distance_matrix[idx1][idx2] += 1-math.log(g, 4)
                weight_distance_matrix[idx2][idx1] += 1-math.log(g, 4)
    return weight_distance_matrix


def pmi(weight_distance_matrix, trigger_count_dict):
    """Calculate pmi of two triggers

    pmi(w1, w2) = P_dist(w1, w2) / P(w1)P(w2)

        P_dist(w1, w2) =
        P(w1) =

    :param weight_distance_matrix:
    :param trigger_count_dict:
    :return:
    """

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