import unittest
from ESIServer.model.Word import WordUnit


class Triple:

    def __init__(self, entity1_list, relationship_list, entity2_list, num=0, doc_num=0, sent_num=0):
        """
        关系三元组，entity和relationship都可能是由多个word组成
        :param doc_num: int
        :param sent_num: int
        :param entity1_list: WordUnit list
        :param relationship_word: WordUnit list
        :param entity2_list: WordUnit list
        """
        self.num = num
        self.doc_num = doc_num
        self.sent_num = sent_num
        if isinstance(entity1_list, list):
            self.entity1_list = entity1_list
        else:
            self.entity1_list = [entity1_list]
        if isinstance(relationship_list, list):
            self.relationship_list = relationship_list
        else:
            self.relationship_list = [relationship_list]
        if isinstance(entity2_list, list):
            self.entity2_list = entity2_list
        else:
            self.entity2_list = [entity2_list]

    def generalize(self):
        pass


    def to_string(self):
        return "DocID: {:>5d}, SentenceID: {:5>d}, Num: {:5>d}, E1: {:s}, Rel: {:s}, E2: {:s}".format(
            self.doc_num,
            self.sent_num,
            self.num,
            ''.join([word.lemma for word in self.entity1_list]),
            ''.join([word.lemma for word in self.relationship_list]),
            ''.join([word.lemma for word in self.entity2_list])
        )

    def __str__(self):
        return "[{}, {}, {}]".format(
            ''.join([word.lemma for word in self.entity1_list]),
            ''.join([word.lemma for word in self.relationship_list]),
            ''.join([word.lemma for word in self.entity2_list])
        )

    __repr__ = __str__  # 控制台输出时默认调用



class TESTTriple(unittest.TestCase):

    def test_seq(self):
        e1 = WordUnit(1, "美国", "nh")
        relationship = WordUnit(2, "总统", 'n')
        e2 = WordUnit(3, "特朗普", 'ni')
        t = Triple(1, 1, e1, relationship, e2)
        print(t)


        import json
        # JSON 序列化对象
        class TT:
            def __init__(self, name):
                self.name = name
        ## 1. 构造函数
        def obj_2_json(obj):
             return {
                 "name": obj.name
             }
        o = TT(name="aaa")
        json.dumps(o, default=obj_2_json)
        ## 2. 使用lambda
        json.dumps(o, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)


        # JSON反序列化对象
        json_str = '{"name":"tt"}'
        def handle(d):
            return TT(d['name'])
        json.loads(json_str, object_hook=handle)


