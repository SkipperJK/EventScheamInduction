import logging
from ESIServer.utils.utils import is_entity
from ESIServer.model.EntityPair import EntityPair
from ESIServer.component.open_relation_extraction.extract_by_dsnf import ExtractByDSNF


debug_logger = logging.getLogger('debug')
root_logger = logging.getLogger('root')
class Extractor:
    """抽取生成知识三元组
    以句子为单位，从句子中找出所有的entity pairs，使用制定好的规则DSNF判断entity pair是否可以构成一个知识三元组
    如果可以，提取出entity pair的relationship。
    Attributes:
        entities: WordUnit list，句子的实体列表
        entity_pairs: EntityPair WordUnit list，句子实体对列表
    """
    entities = []  # 存储该句子中的可能实体
    entity_pairs = []  # 存储该句子中(满足一定条件)的可能实体对

    # def extract(self, origin_sentence, sentence, file_path, num):
    def extract(self, origin_sentence, sentence):
        """
        Args:
            origin_sentence: string，原始句子
            sentence: SentenceUnit，句子单元
        Returns:
            num： 知识三元组的数量编号
        """
        self.triples = []
        self.get_entities(sentence)
        self.get_entity_pairs(sentence)
        debug_logger.debug('Entities: {}'.format(list(map(str, self.entities))))  # # print list并不会调用list的元素的__str__
        debug_logger.debug('Entity pairs: {}'.format(list(map(str, self.entity_pairs))))

        for i, entity_pair in enumerate(self.entity_pairs):
            debug_logger.debug("分析实体对儿{:>3d}： {:s}".format(i, str(entity_pair)))
            debug_logger.debug(sentence.has_extracted)
            entity1 = entity_pair.entity1
            entity2 = entity_pair.entity2
            id1 = entity1.ID-1
            id2 = entity2.ID-1
            if sentence.has_extracted[id1] == True or sentence.has_extracted[id2]:
                debug_logger.debug("{:s} is extracted by 偏正结构, continue...".format(
                    str(entity1) if sentence.has_extracted[id1] else str(entity2)
                ))
                continue

            extract_dsnf = ExtractByDSNF(origin_sentence, sentence, entity1, entity2)
            # ? 一个entity pair可能提取出多个triples吗？
            # [DSNF2|DSNF7]，部分覆盖[DSNF5|DSNF6]
            if extract_dsnf.SBV_VOB(entity1, entity2):
                pass
            # [DSNF4]
            if extract_dsnf.SBV_CMP_POB(entity1, entity2):
                pass
            if extract_dsnf.SBVorFOB_POB_VOB(entity1, entity2):
                pass
            # [DSNF1]
            if not extract_dsnf.E_NN_E(entity1, entity2):
                pass
            # [DSNF3|DSNF5|DSNF6]，并列实体中的主谓宾可能会包含DSNF3
            if extract_dsnf.coordinate(entity1, entity2):
                pass
            # ["的"短语]
            if extract_dsnf.entity_de_entity_NNT(entity1, entity2):
                pass
            if extract_dsnf.triples != None:
                self.triples.extend(extract_dsnf.triples)
        return self.triples

    def get_entities(self, sentence):
        """获取句子中的所有可能实体
        通过只抽取与某些指定类型的实体：人名，机构名，地名等，---》过滤掉很多无意义的信息
        例如：习近平主席和李克强总理接见普京。 --》实体：['习近平', '李克强', '普京']，不会单独的寻找'总统'相关的信息
        Args:
            sentence: SentenceUnit，句子单元
        Returns:
            None
        """
        self.entities.clear()  # 清空实体
        for word in sentence.words:
            if is_entity(word):
                self.entities.append(word)

    def get_entity_pairs(self, sentence):
        """组成实体对，限制实体对之间的实体数量不能超过4
        Args:
            sentence: SentenceUnit，句子单元
        """
        self.entity_pairs.clear()  # 清空实体对
        length = len(self.entities)
        i = 0
        while i < length:
            j = i + 1
            while j < length:
                if (self.entities[i].lemma != self.entities[j].lemma and
                    self.get_entity_num_between(self.entities[i], self.entities[j], sentence) <= 4):
                    self.entity_pairs.append(EntityPair(self.entities[i], self.entities[j]))
                j += 1
            i += 1

    def get_entity_num_between(self, entity1, entity2, sentence):
        """获得两个实体之间的实体数量
        Args:
            entity1: WordUnit，实体1
            entity2: WordUnit，实体2
        Returns:
            num: int，两实体间的实体数量
        """
        num = 0
        i = entity1.ID + 1
        while i < entity2.ID:
            if is_entity(sentence.words[i]):
                num += 1
            i += 1
        return num
