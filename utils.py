# -*- coding: utf-8 -*-

"""
@project: custom words similarity
@author: David
@time: 2021/8/20 15:13
"""
import re
import os
import json
import numpy as np


class Utils(object):
    def __init__(self):
        pass

    #问题：静态方法在内存中的类是单例的吗？
    @staticmethod
    def fetch_chinese(word):
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        chinese = re.sub(pattern, '', word)
        return chinese

    @staticmethod
    def write(data, fileName):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # 获取excel所在文件目录
        result = os.path.join(dir_path, 'data', fileName)
        with open(r'{}'.format(result), 'w', encoding='utf-8') as f:
            qd = json.dumps(data, ensure_ascii=False)  # Json序列化
            f.write(qd)
            f.close()

    @staticmethod
    def read(fileName):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # 获取excel所在文件目录
        path = os.path.join(dir_path, '语料', fileName)
        with open(path, 'r', encoding='utf-8') as load_f:
            result = json.load(load_f)
        return result


dir_path = os.path.dirname(os.path.realpath(__file__))
def writeEmb(path, datas):
    with open(r'{}'.format(path), 'w', encoding='utf-8') as f:
        for key, value in datas.items():
            new_value = map(lambda x:str(x), value)
            f.write(key+'\t'+",".join(new_value)+'\n')
        f.close()

def writeStr(path, strs):
    with open(r'{}'.format(path), 'w', encoding='utf-8') as f:
        f.write(strs)
        f.close()

def writeJson(path, data):
    with open(r'{}'.format(path), 'w', encoding='utf-8') as f:
        qd = json.dumps(data, ensure_ascii=False)  # Json序列化
        f.write(qd)
        f.close()

def readLines(path):
    with open(path, encoding='utf-8') as f:
        result = f.readlines()
        return result

def readDict(path):
    with open(path, 'r', encoding='utf-8') as load_f:
        result = json.load(load_f)
    return result
