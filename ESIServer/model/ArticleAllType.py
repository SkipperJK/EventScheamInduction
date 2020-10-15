from mongoengine import connect
from mongoengine.fields import *
from mongoengine.document import *


# __all__ = (
#     "OriginalArticle"
# )

connect(alias="ReadOrigin", db="Sina", host='10.141.223.31', port=27017)
# disconnect(alias='ReadOrigin')

class ArticleAllType(Document):
    meta = {
        'db_alias': 'ReadOrigin',
        'collection': 'article20191121'
    }

    _id = ObjectIdField()
    title = StringField(required=True)
    url = URLField()
    content = StringField(required=True)
    time = DateField()
    media_show = StringField()
    thumb = URLField()
    mediaL = IntField()
    qscore = IntField()

    # sentences = None


class ArticleEntertainment(Document):
    meta = {
        'db_alias': 'ReadOrigin',
        'collection': 'article20190413_sim'
    }
    _id = ObjectIdField()
    title = StringField()
    url = URLField()
    content = StringField()
    code = StringField()
    time = StringField()
    source = StringField()
    channel = StringField()
    types = ListField()
    tags = ListField()
    imgUrls = ListField()



class ArticleInternational(Document):
    meta = {
        'db_alias': 'ReadOrigin',
        'collection': 'article20190422'
    }
    _id = ObjectIdField()
    title = StringField()
    url = URLField()
    content = StringField()
    code = StringField()
    time = StringField()
    source = StringField()
    channel = StringField()
    types = ListField()
    tags = ListField()
    imgUrls = ListField()


if __name__ == '__main__':
    for i, article in enumerate(ArticleAllType.objects):
        print(i, article['title'])
        break

    for i, article in enumerate(ArticleEntertainment.objects):
        print(i, article['title'])
        break

    for i, article in enumerate(ArticleInternational.objects):
        print(i, article['title'])
        break


