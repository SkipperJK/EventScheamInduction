import sys
sys.path.append("../")
from pyhanlp import *
from mongoengine import connect
from ESIServer.model.ArticleAllType import ArticleAllType
from ESIServer.utlis.split_sentence import split_sentence
from ESIServer.model.Sentence import Sentence
from ESIServer.model.Word import Word
from ESIServer.model.Article import Article


# print(type(HanLP.segment('你好，欢迎在Python中调用HanLP的API')))
# print(type(HanLP.parseDependency('你好，欢迎在Python中调用HanLP的API')))
# for term in HanLP.segment("你好，欢迎在Python中调用HanLP的API"):
#     print(term.word, term.nature, term.offset)

'''Hanlp 依存句法分析结果
word.ID         ID      当前词在句子中的序号，１开始
word.LEMMA      LEMMA   当前词语（或标点）的原型或词干，在中文中，此列与FORM相同
word.CPOSTAG    CPOSTAG 当前词语的词性（粗粒度）
word.POSTAG     POSTAG  当前词语的词性（细粒度）
word.HEAD.ID    HEAD    当前词语的中心词
word.DEPREL     DEPREL  当前词语与中心词的依存关系
word.NAME       NAME    等效字符串

例子：
你好，欢迎在Python中调用HanLP的API
 ID      LEMMA    CPOSTAG     POSTAG HEAD.ID     DEPREL       NAME
  1         你好          i          l   0       核心关系         你好
  2          ，         wp          w   1       标点符号          ，
  3         欢迎          v          v   1       并列关系         欢迎
  4          在          p          p   7       状中结构          在
  5     Python         ws         nx   6       定中关系       未##专
  6          中         nd          f   4       介宾关系          中
  7         调用          v          v   3       动宾关系         调用
  8      HanLP         ws         nx   7       动宾关系       未##专
  9          的          u          u   7      右附加关系          的
 10        API         ws         nx   3       动宾关系       未##专
 
ID从1开始，
'''
# print("%3s %10s %10s %10s %3s %10s %10s" % ('ID', 'LEMMA', 'CPOSTAG', 'POSTAG', 'HEAD.ID', 'DEPREL', 'NAME'))
# for word in HanLP.parseDependency("你好，欢迎在Python中调用HanLP的API"):
#     print("%3d %10s %10s %10s %3d %10s %10s" % (word.ID, word.LEMMA, word.CPOSTAG, word.POSTAG, word.HEAD.ID, word.DEPREL, word.NAME))

# 最好用
if __name__ == '__main__':
    docs = []


    for i, doc in enumerate(ArticleAllType.objects[10:].batch_size(1).timeout(False)):
        try:
            print(i, doc['title'])
            if Article.objects(_id=doc['_id']):
                print("exist")
            sents = []
            for sent in split_sentence(doc['content']):
                words = []
                if len(sent) < 6 and len(sent) > 100:
                    continue
                for word in HanLP.parseDependency(sent):
                    words.append(Word(id=word.ID, lemma=word.LEMMA, cpostag=word.CPOSTAG, postag=word.POSTAG, head_id=word.HEAD.ID, dependency=word.DEPREL, name=word.NAME))
                sents.append(Sentence(sentence=sent, words=words))
            doc = Article(_id=doc['_id'], title=doc['title'], sentences=sents)
            doc.save()   # 如果数据库中已有相同的_id，会覆盖之前的数据。
            # docs.append()
            if i> 100000:
                break
        except Exception as e:
            print(e)

