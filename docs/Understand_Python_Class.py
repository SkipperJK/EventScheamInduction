from mongoengine import connect
from mongoengine.fields import *
from mongoengine.document import Document, DynamicDocument, DynamicEmbeddedDocument, EmbeddedDocument, EmbeddedDocumentList

# 1. MongoEngine
# 2. Document
# 3. DynamicDocument, DynamicEmbeddedDocument

connect(alias="Test", db="Test", host="10.132.141.255", port=27017)

'''
通过MongoEngine允许您为文档定义模式（schema），因为这有助于减少编码错误，并定义了字段（field）类。
    要为文档定义模式，请创建一个从Document继承的类。通过将字段对象作为类属性添加到文档类来指定字段。
        Filed都是类，因此自定义的model中，类变量都是Filed类的实例，都是不可变类型，修改自定义model的实例对象只对自身产生副作用，对其他实例没有影响。
    由于BSON（用于在mongodb中存储数据的二进制格式）与顺序有关，因此文档将根据其字段顺序进行序列化。
 
'''

class Test1(Document):

    meta = {
        'db_alias': "Test",
        'collection': 'test1'
    }

    name = StringField()  # 注意如果定义 id 字段，会自动存为 auto_id_0
    count = IntField()
    imgs = ListField(default=None)  # default=None 创建实例的时候，没有定义则不会写入
    other = StringField()  # 默认 default=None
    dd = []
    # test = Document("Test1")

'''
类中：StringField(), IntField()... 都是类
    类的实例对象是不可变对象。
'''
'''
类中没有定义__init__()函数，在实例化时会调用父类的__init__()函数，实例化时的参数要符合父类__init__()函数的参数。

'''
a = Test1(name="jklkjk", count=10, imgs=['1111', '2222', '3333'])  # 参数必须是mongoengine中定义的Field
b = Test1(name='qqqq', count=100)   # 可以缺少，save的时候使用默认值，也可以使用参数 default来这是Filed的默认值。
print(a.imgs)
print(b.imgs)
a.dd.append(1)
print(a.dd)
print(b.dd)
a.addNew  = "add new filed don't store to mongo"
a.save()  # dd字段并没有存储到mongo中。
b.save()






'''
类中，定义了__init__()函数，并使用super()执行父类的__init__()函数
    在save()时，之后为Field的类属性才会存储到Mongodb中。如果想要存储非Field属性，需要使用继承 DynamicDocument 类
'''
class Test2(Document):

    meta = {
        'db_alias': 'Test',
        'collection': "test2"
    }

    # id = StringField() # 其要是ObjectField对象
    name = StringField()
    count = IntField()
    imgs = ListField()
    dd = []

    def __init__(self, x, *args, **values):
        super().__init__(*args, **values)
        self.x = 10

t21 = Test2(name="jklkjk", count=10, imgs=['1111', '2222', '3333'], x=10)  # 参数必须是mongoengine中定义的Field
t22 = Test2(name='qqqq', count=100, imgs=['qqq', 'www', 'eee'], x=100)
t21.save()







'''DynamicDocument
Note: DynamicDocument的字段不能以 下划线_ 开头
动态的文档类型，当类实例额外添加数据属性的使用，执行save()函数时，也会把添加的属性存储到mongo中。
'''
class Test3(DynamicDocument):

    meta = {
        'db_alias': 'Test',
        'collection': 'test3'
    }

    name = StringField()
    ref = ReferenceField(Test2)   # 存储的是引用对象在mongodb中的ObjectID
    # ref = GenericReferenceField()   # 不需要指定Document

t31 = Test3(name="DynamicDocument", ref=t21)
t32 = Test3(name="add filed", ref=t22)
# t31.borther = t31  # 会造成循环递归
# t31.borther = t32
t31.tags = ['add new attribute']   # 会存储到MongoDB中去。
t31.save()
# t32.save()   # ou can only reference documents once they have been saved to the database: ['ref']
# 也就是引用对象必须是已经存储在mongodb中的。
# t32.save(cascade=True) # 不是存储被存储的意思




'''
自定义主键： 真实存储字段名替换为 _id
'''
class Test4(Document):

    meta = {
        'db_alias': "Test",
        'collection': 'test4'
    }

    name = StringField(primary_key=True)  # 定义主键之后，字段name会在数据库中存储为 "_id"
    count = IntField()

t41 = Test4(name="primary_key", count=10)
t41.save()




class Test5(EmbeddedDocument):
    name = StringField()
    dep = EmbeddedDocumentField("Test5")
    dep1 = EmbeddedDocumentField("self")

class Test6(Document):
    meta = {
        'db_alias': 'Test',
        'collection': 'test6'
    }
    sent = StringField()
    words = EmbeddedDocumentListField(Test5, default=None)

t51 = Test5(name = "t51")
t52 = Test5(name = "t52")
t53 = Test5(name = "t53")
t51.dep = t52
t51.dep1 = t53
t61 = Test6(sent="Test EmbeddedDocument nested", words=[t51, t52, t53])
t62 = Test6(sent="default is effect????")
t61.save()
t62.save()


'''
Query:
1. filtering queries
2. limiting and skipping 
3. query efficient
    Retrieving a subset of fields
    
Class.objects 返回的是一个QuerySet类对象，QuerySet类继承了BaseQuerySet类，该类中定义timeout等等方法。
'''

for i in Test1.objects[1:].only('name').timeout(False):
    print(i.name, i['name'])


