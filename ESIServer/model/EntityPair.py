from unittest import TestCase
from ESIServer.model.Word import WordUnit
class EntityPair:
    """实体对
    Atrributes:
        entity1: WordUnit，实体1的词单元
        entity2: WordUnit，实体2的词单元
    """
    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

    def get_entity1(self):
        return self.entity1
    def set_entity1(self, entity1):
        self.entity1 = entity1

    def get_entity2(self):
        return self.entity2
    def set_entity2(self, entity2):
        self.entity2 = entity2

    def __str__(self):
        return "{{E1:{0:{2}>10s}, E2:{1:{2}>10s}}}".format(
            self.entity1.lemma,
            self.entity2.lemma,
            chr(12288))


class TESTEntityPair(TestCase):
    def test_output(self):
        word1 = WordUnit(0, '中国', 'ns', 'Ns',  0, None, '')
        word2 = WordUnit(1, '北京', 'ns', 'Ns',  0, None, '')
        entitypair = EntityPair(word1, word2)
        print(entitypair)