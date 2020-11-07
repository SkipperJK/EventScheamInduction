import unittest
from ESIServer.model.Word import WordUnit


class Triple:

    def __init__(self, entity1_list, relationship_list, entity2_list, num=0, doc_num=0, sent_num=0):
        """
        关系三元组，entity和relationship由单个/多个word组成，将单个的也转换为list
        :param doc_num: int
        :param sent_num: int
        :param entity1_list: WordUnit list / WordUnit
        :param relationship_word: WordUnit list / WordUnit
        :param entity2_list: WordUnit list / WordUnit
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

        self.e1_lemma = ''.join([word.lemma for word in self.entity1_list])
        self.relation_lemma = ''.join([word.lemma for word in self.relationship_list])
        self.e2_lemma = ''.join([word.lemma for word in self.entity2_list])
        self.generalization()

    def generalization(self):
        """
        关系元组一般化，记录元组中两个实体的命名实体类型
        :return:
        """
        self.entity1_nertype = ''
        self.entity2_nertype = ''
        nertag2type = {'Nh':'person', 'Ns':'location', 'Ni':'organization'}
        for entity in self.entity1_list:
            if entity.nertag:
                self.entity1_nertype = nertag2type[entity.nertag]
                break
        for entity in self.entity2_list:
            if entity.nertag:
                self.entity2_nertype = nertag2type[entity.nertag]
                break


    def to_string(self):
        return "DocID: {0:>5d}, SentenceID: {1:>3d}, Num: {2:2d}, {3:s}".format(
            self.doc_num,
            self.sent_num,
            self.num,
            str(self)
        )


    def __str__(self):
        # 使用中文空格 chr(12288) 填充，实现中文对齐
        return "(E1: {0:{6}>10s}, Rel: {1:{6}>10s}, E2: {2:{6}>10s}), Generalization: <{3:s}>, {4:s}, <{5:s}>".format(
            self.e1_lemma,
            self.relation_lemma,
            self.e2_lemma,
            self.entity1_nertype,
            self.relation_lemma,
            self.entity2_nertype,
            chr(12288)
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


