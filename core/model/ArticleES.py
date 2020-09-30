from collections import namedtuple

class ArticleES:

    def __init__(self, title, content, time):
        self.title = title
        self.content = content
        self.time = time


def customAritcleESDecoder(articleDict):
    """
    convert json(str) to ArticleES object
    :param articleDict:
    :return:
    """
    return namedtuple("ArticleES", articleDict.keys())(*articleDict.value())
    # namedtuple是一个函数，相当于执行函数返回函数的返回值