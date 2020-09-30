from mongoengine import connect
from mongoengine.fields import *
from mongoengine.document import Document
from mongoengine.document import EmbeddedDocument
# from core.model.Sentence import Sentence


connect(alias="WriteResult", db="SinaNews", host="10.132.141.255", port=27017)

class Article(Document):

    meta = {
        'db_alias': "WriteResult",
        'collection': "result_20191121"
    }

    _id = ObjectIdField()
    title = StringField()
    sentences = EmbeddedDocumentListField(Sentence, default=[])  # 避免将[] 存入


class Sentence(EmbeddedDocument):

    sentence = StringField()
    words = EmbeddedDocumentListField(Word, default=None)  # 避免将[]存入，但是当创建实例时不能指定该参数


class Word(EmbeddedDocument):

    id = IntField()
    lemma = StringField()
    cpostag = StringField()
    postag = StringField()
    head_id = IntField()
    head_word = EmbeddedDocumentField("Word")   # 无法这样使用
    dependency = StringField()
    name = StringField()




if __name__ == '__main__':
    for i, article in enumerate(Article.objects):
        print(i, article.title)
        break

