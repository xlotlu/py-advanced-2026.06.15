import sqlite3

class Processor:
    _object = None
    _inited = False

    # classmethod implicit
    def __new__(cls, *args, **kwargs):
        # __new__ returnează un obiect instanțiat

        if cls._object is None:
            cls._object = super().__new__(cls, *args, **kwargs)

        return cls._object

    def __init__(self):
        # aici există self
        if self._inited:
            return
        self._inited = True
        print("» init")

    def method(self):
        pass


class SqliteConnection:
    _objects = {}
    _inited = False

    # classmethod implicit
    def __new__(cls, filename):
        # __new__ returnează un obiect instanțiat

        if filename in cls._objects:
            return cls._objects[filename]
        
        object = super().__new__(cls)
        object.conn = sqlite3.connect(filename)
        cls._objects[filename] = object

        return object

    def __init__(self, filename):
        pass



class MyMeta(type):
    def __new__(mcls, name, bases, namespace):
        # class object creation
        # for ezoteric usecases (pydantic, django orm, ...)
        return super().__new__(mcls, name, bases, namespace)
        # ^^ tocmai am returnat o clasă!

    def __init__(cls, name, bases, namespace):
        # cls este acum o clasă!
        cls.y = 30

    def __call__(cls, *args, **kwargs):
        # aici fac o instanță nouă (obiectul propriu-zis) din acest cls
        print("» în call")
        print(args)
        print(kwargs)

        # by default aceasta trigger-uiește
        # cls.__new__() și apoi cls.__init__()
        obj = super().__call__(*args, **kwargs)
        # îl customizezi pe obj 
        return obj


class MyCls(metaclass=MyMeta):
    x = 15
    y = 20

    def __init__(self, arg):
        pass


# putem să facem o metaclasă ce transformă în singleton
# oricare clasă căreia îi este atașată?



class MultitonMeta(type):
    # avem de așezat instanțe de SqliteConnection()
    # asociate la filename-ul lor

    _instances = {}

    def __call__(cls, *args, **kwargs):
        # we build a unique key
        # for the combination of class
        # and its args & kwargs
        key = (cls, *args, *kwargs.items())

        try:
            obj = cls._instances[key]
        except KeyError:
            obj = cls._instances[key] = super().__call__(*args, **kwargs)
            
        return obj


class SqliteConnection(metaclass=MultitonMeta):
    def __init__(self, filename, options, stuff=235):
        print("» init", filename, options, stuff)
        self.conn = sqlite3.connect(filename)

"""
SqliteConnection("whatever.db", "options", stuff=2)
SqliteConnection("whatever.db", "options", stuff=2)

SqliteConnection("whateverx.db", "options", stuff=2)
SqliteConnection("whateverx.db", "options", stuff=2)

SqliteConnection("whateverx.db", "optionZ", stuff=2)
SqliteConnection("whateverx.db", "optionZ", stuff=2)

SqliteConnection("whateverx.db", "optionZ", stuff=5)
SqliteConnection("whateverx.db", "optionZ", stuff=5)
"""


# full flow
"""
class Meta(type):
    def __new__(mcls, *args, **kwargs):
        print('» meta new')
        return super().__new__(mcls, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        print('» meta init')
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('» meta call')
        return super().__call__(*args, **kwargs)
    
class Cls(metaclass=Meta):
    def __new__(cls, *args, **kwargs):
        print('» class new')
        return super().__new__(cls, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        print('» class init')
        super().__init__(*args, **kwargs)

#Cls()
"""

