# -*- coding: utf-8 -*-

"""
@project: custom words similarity
@author: David
@http: https://blog.csdn.net/qq_39451578/article/details/104474450
@http: https://www.cnblogs.com/caiyishuai/p/9511567.html
@time: 2021/10/30 13:11
"""
# coding:utf-8
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from utils import Utils, writeStr, writeEmb, readDict
import jieba
import os
import time


def separate(documents):
    all = []
    entities = []
    for key, value in documents.items():
        docs = []
        for doc in value:
            sentences = doc.split('-:-')
            for sen in sentences:
                sen1 = Utils.fetch_chinese(sen)
                docs.extend(list(jieba.cut(sen1)))
        all.append(docs)
        entities.append(key)
    return all, entities


def filter_stopwords(path, all):
    stopwords = []
    with open(path, 'r', encoding='utf-8') as load_f:
        for line in load_f.readlines():
            stopwords.append(line[:-1])
    for x, doc in enumerate(all):
        one_doc = []
        for word in doc:
            if word not in stopwords:
                one_doc.append(word)
            # else:
            #     print("在第%d篇文档里，有停用词%s" % (x, word))
        all[x] = one_doc
    return all


def distinct(all, entities):
    delete_nums = []
    for i, al in enumerate(all):
        if len(al) == 0:
            delete_nums.append(int(i))
    entities = [entities[i] for i in range(0, len(all), 1) if len(all[i]) != 0]
    all = [all[i] for i in range(0, len(all), 1) if len(all[i]) != 0]
    return entities, all

class TFIDF(object):
    def __init__(self, document, entities):
        self.document = document
        self.entities = entities
        tfidf_model = TfidfVectorizer().fit(self.document)
        self.feature = tfidf_model.get_feature_names()
        self.sparse_result = tfidf_model.transform(self.document)
        self.weight = self.sparse_result.toarray()


    def construct_keywords(self):
        # 构建词与tf-idf的字典：
        keywords = {}
        fres = {}
        for i in range(len(self.weight)):
            one_doc_fre = {}
            feature_TFIDF = {}
            for j in range(len(self.feature)):
                if self.feature[j] not in feature_TFIDF:
                    if self.weight[i][j] != 0.0:
                        feature_TFIDF[self.feature[j]] = self.weight[i][j]
                else:
                    print("不该进入这个方法！")
                    feature_TFIDF[self.feature[j]] = max(feature_TFIDF[self.feature[j]], self.weight[i][j])
                    break
            # print('TF-IDF 排名前5的：')
            featureList = sorted(feature_TFIDF.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            # print("featureList的长度为：", len(featureList))
            fea = len(featureList)
            m = 0
            if fea > 500:
                m = 10
            elif 500 >= fea > 50:
                m = 5
            elif 50 >= fea > 15:
                m = 3
            elif 15>= fea > 10:
                m = 2
            else:
                m = 1
            if len(featureList) != 0:
                for k in range(0, 5 if len(featureList) > 10 else 1):
                    # print(featureList[k][0], featureList[k][1])
                    keywords.setdefault(self.entities[i], []).append(featureList[k][0])
                    # if featureList[k][0] in keys:
                    #     print(keys[featureList[k][0]], featureList[k][1])
                    one_doc_fre[featureList[k][0]] = float('%.5f'%featureList[k][1])
                    # keys.append(featureList[k][0])
                    fres[self.entities[i]] = one_doc_fre
            else:
                # print("xxxxxxxxxxxxxxxxxxx")
                print("文档", self.entities[i], "没有特征，其内容为：", self.document[i])

        return keywords, fres


if __name__ == '__main__':
    start = time.time()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'data', 'canopy聚类文档(0.8,0.86).txt')
    stopP = os.path.join(dir_path, 'data', '哈工大停用词表.txt')
    docs = readDict(path)

    all, entities = separate(documents=docs)
    all = filter_stopwords(stopP, all=all)
    entities, all = distinct(all, entities)

    document = [" ".join(sent0) for sent0 in all]

    tf = TFIDF(document=document, entities=entities)
    keywords, keys = tf.construct_keywords()

    end = time.time()
    print('生成TFIDF的时间time: {}s'.format(end - start))
