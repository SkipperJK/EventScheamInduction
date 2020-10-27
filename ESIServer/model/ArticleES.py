from ESIServer.utils.utils import split_sentence
from collections import namedtuple

class ArticleES:

    def __init__(self, title, content, time):
        self.title = title
        self.content = content
        self.time = time

    @property
    def sentence_of_title(self):
        return split_sentence(self.title)

    @property
    def sentence_of_content(self):
        return split_sentence(self.content)






def customAritcleESDecoder(articleDict):
    """
    convert json(str) to ArticleES object
    :param articleDict:
    :return:
    """
    return namedtuple("ArticleES", articleDict.keys())(*articleDict.value())
    # namedtuple是一个函数，相当于执行函数返回函数的返回值