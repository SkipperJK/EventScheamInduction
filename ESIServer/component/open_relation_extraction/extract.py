import unittest
from ESIServer.component.open_relation_extraction.nlp import NLP
from ESIServer.component.open_relation_extraction.extractor import Extractor

nlp = NLP()
extractor = Extractor()


def extract(origin_sentences):
    lemmas, hidden = nlp.segment(origin_sentences)
    words_postag = nlp.postag(lemmas, hidden)
    words_nertag = nlp.nertag(words_postag, hidden)
    sentences = nlp.dependency(words_nertag, hidden)
    num = 0
    for idx_sent, sent in enumerate(origin_sentences):
        print('+' * 30)
        print(sent)
        for word in sentences[idx_sent].words:
            print(word.__dict__)
        print('-' * 30)
        print(extractor.extract(sent, sentences[idx_sent], './', num))



class TestExtract(unittest.TestCase):
    """
    继承unittest.TestCase，类的成员变量以test的开头的被认为是测试方法，测试时会执行
    """

    def test_extract(self):
        origin_sentences = [
            "李克强总理今天来我家了，我赶紧往家里跑。",
            "浮士德与魔鬼达成协议。",
            "巴拿马在2007年与中国建立关系。",
            "德国总统高克。",
            "高克访问中国。",
            "习近平在上海视察。",
            "习近平对埃及进行国事访问。",
            "奥巴马毕业于哈佛大学。",
            "习近平主席和李克强总理接见普京。",
            "习近平访问了美国和英国。",
            "高克访问中国，并在同济大学发表演讲。"
        ]

        extract(origin_sentences)