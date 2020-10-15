
class Triple:

    def __init__(self, doc_num, sent_num, word, sub, obj):
        self.doc_num = doc_num
        self.sent_num = sent_num
        self.word = word
        self.sub = sub
        self.obj = obj


    def __str__(self):
        # return f''  # f-string format
        return "docID: %d, SentenceID: %d, verb: %s, sub: %s, obj: %s" % (self.doc_num, self.sent_num, self.word, self.sub, self.obj)

    __repr__ = __str__  # 控制台输出时默认调用

if __name__ == '__main__':
    t = Triple(10, 1, 'vvv', 'sss', 'ooo')
    print(t)

    import json

    # JSON 序列化对象
    class TT:
        def __init__(self, name):
            self.name = name
    # 1. 构造函数
    def obj_2_json(obj):
         return {
             "name": obj.name
         }
    o = TT(name="aaa")
    json.dumps(o, default=obj_2_json)

    # 2. 使用lambda
    json.dumps(o, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)


    # JSON反序列化对象
    json_str = '{"name":"tt"}'
    def handle(d):
        return TT(d['name'])
    json.loads(json_str, object_hook=handle)


