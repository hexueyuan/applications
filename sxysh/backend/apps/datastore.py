# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from os.path import realpath
from contextlib import contextmanager

from json import dumps

__all__ = ['Model', 'Store', 'setup']

class TableNamespace:
    """存放数据表类的结构，该类代表一个数据库表命名空间，被Model引用
    """
    __table = {}

    def add(self, name, tableModel):
        """往一个数据库命名空间添加一个数据表
        """
        self._TableNamespace__table[name] = tableModel
    
    def __getattr__(self, key):
        """重定义属性引用方式，当不存在时抛出错误
        """
        if self._TableNamespace__table.has_key(key):
            return self._TableNamespace__table.get(key)
        else:
            raise NameError("table '%s' is not exists." % key)

    def __getitem__(self, key):
        """重定义属性引用方式，当不存在时抛出错误
        """
        if self._TableNamespace__table.has_key(key):
            return self._TableNamespace__table.get(key)
        else:
            raise NameError("table '%s' is not exists." % key)
    
    def __repr__(self):
        repr_dict = {k:v.__name__ for k, v in self._TableNamespace__table.items()}
        return dumps(repr_dict, indent=2)


class ModelBase:
    """存放全部数据库命名空间，一个项目中允许多个数据库存在，引用数据表类时需要指定数据库名和数据表名
    """
    __models = {}

    def add(self, name, tname, tclass):
        # 向一个指定的数据库命名空间添加一个数据表，当数据库命名空间不存在时创建该空间
        if not self._ModelBase__models.has_key(name):
            self._ModelBase__models[name] = TableNamespace()
        self._ModelBase__models[name].add(tname, tclass)

    def __getattr__(self, key):
        # 重定义属性引用方式
        if self._ModelBase__models.has_key(key):
            return self._ModelBase__models.get(key)
        else:
            raise NameError("table namespace '%s' is not exists." % key)
    
    def __getitem__(self, key):
        # 重定义属性引用方式
        if self._ModelBase__models.has_key(key):
            return self._ModelBase__models.get(key)
        else:
            raise NameError("table namespace '%s' is not exists." % key)

    def __repr__(self):
        repr_dict = {k:str(v) for k, v in self._ModelBase__models.items()}
        return dumps(repr_dict, indent=2)


# 全局对象，被外部引用
Model = ModelBase()


class StoreBase:
    """数据库引擎管理
    """
    __stores = {}

    def add(self, name, engine):
        self._StoreBase__stores[name] = engine

    def get(self, key):
        if self._StoreBase__stores.has_key(key):
            return self._StoreBase__stores.get(key)
        else:
            raise NameError("store %s is not exists." % key)

    @contextmanager
    def __getattr__(self, key):
        if self._StoreBase__stores.has_key(key):
            session = sessionmaker(bind=self._StoreBase__stores.get(key))()
            yield session
            session.close()
        else:
            raise NameError("store %s is not exists." % key)

    @contextmanager
    def __getitem__(self, key):
        if self._StoreBase__stores.has_key(key):
            session = sessionmaker(bind=self._StoreBase__stores.get(key))()
            yield session
            session.close()
        else:
            raise NameError("store %s is not exists." % key)
    
    def __repr__(self):
        repr_dict = {k:v.__name__ for k, v in self._StoreBase__stores.items()}
        return dumps(repr_dict, indent=2)


# 全局Store对象
Store = StoreBase()


# 数据库工厂类
class ManageBase:
    def __init__(self, model, store, conf):
        """构造ManageBase
        """
        self.__models = model
        self.__stores = store
        self.__conf = conf

    def setup(self):
        """
        根据配置进行初始化
        conf定义见[How to use datastore](mylib/test/dashboard/use_datastore.py)
        """
        for name, cfg in self._ManageBase__conf.items():
            # 根据配置创建数据库引擎以及数据表
            self._ManageBase__createone(name, cfg)

    def __createone(self, sname, cfg):
        """
        sname -> store name
        cfg   -> configuration
        just support sqlite now.
        创建一个数据库引擎，当前版本仅支持SQLite
        创建数据库引擎的数据表
        """
        if cfg[u'type'] == "sqlite":
            path = cfg[u'path']
            engine = create_engine('sqlite:///' + realpath(path))
            self._ManageBase__stores.add(sname, engine)
        else:
            # TODO:more type support
            return
        
        # 创建数据表
        base = declarative_base()
        for tname, tcolumns in cfg.get(u'tables', {}).items():
            # 创建数据表类
            tclass = self.__class__._ManageBase__createTable(tname, tcolumns, base)
            # 添加类到Model中供外部引用
            self._ManageBase__models.add(sname, tname, tclass)
        # 创建当前数据库所有定义的数据表
        base.metadata.create_all(self._ManageBase__stores.get(sname))

    @staticmethod
    def __createTable(tname, tcolumns, base):
        """创建并返回一个数据表类
        """
        columnDefine = {
            u'__tablename__': tname,
            u'__repr__': ManageBase.repr
        }
        for c in tcolumns:
            if c.get(u'type') == u"String":
                columnDefine[c.get(u'prop')] = Column(   String(c.get(u'length', 16)),
                                                        nullable=c.get(u'nullable', False),
                                                        primary_key=c.get(u'primary_key', False))
            elif c.get(u'type') == u"Integer":
                columnDefine[c.get(u'prop')] = Column(   Integer,
                                                        nullable=c.get(u'nullable', False),
                                                        primary_key=c.get(u'primary_key', False))
            else:
                pass
        if type(tname) == type(u''):
            tname = tname.encode('utf-8')
        classDefine = type(tname, (base,), columnDefine)
        return classDefine

    @staticmethod
    def repr(obj):
        allattrs = obj.__class__.__dict__
        attrs = [x for x in allattrs.keys() if not x.startswith('_')]
        ra = ""
        for x in attrs:
            ra += x + "="
            if type(getattr(obj, x)) == type(''):
                ra += "'{}'".format(getattr(obj, x))
            else:
                ra += "{}".format(getattr(obj, x))
            ra += ", "
        ra = ra[:-2]
        return "%s(%s)" % (obj.__class__.__name__, ra)


# 全局Manage对象
Manage = None

def setup(conf):
    """配置全局对象Manage
    """
    global Manage, Model, Store
    Manage = ManageBase(Model, Store, conf)
    Manage.setup()
    print "db is setup!"
    print Model._ModelBase__models
    print Store._StoreBase__stores