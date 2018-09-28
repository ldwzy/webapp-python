#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_default

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super().__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v
    
    def __getattr__(self, key):
        try:
            return self[key]
        except:
            raise AttributeError(r"''Dict object has no attribute '%s''" % key) 

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override): #将override配置加入到defaults中并返回该新的字典实例
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):  
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r            
            
def toDict(d): #将字典实例转换成Dict实例，可以以XX.YY方式添加键值对
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v    
    return D    
            
configs = config_default.configs
    
try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)    