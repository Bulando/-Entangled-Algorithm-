# -*- coding: utf-8 -*-

"""
@project: custom words similarity
@author: David
@time: 2021/8/19 8:42
"""
import jieba
from utils import Utils
from tfidf import TFIDF, separate, filter_stopwords, distinct
import time
import os
from utils import readDict, writeJson

class Merge_synonyms(object):
    def __init__(self, dataset, entities):
        tfidf = TFIDF(document=dataset, entities=entities)
        keywords, fres = tfidf.construct_keywords()
        self.param4_fre = keywords
        self.fres = fres
        self.utils = Utils()

    def Co_occurrence_keywords(self):
        keys = [w for v in self.param4_fre.values() for w in v]
        ckeys = set([key for key in keys if keys.count(key) > 1])
        singleKeys = set(keys) - ckeys
        ckeys_mainwords = {}
        ckeys_mainwords_list = []
        for key in ckeys:
            for k, v in self.param4_fre.items():
                if key in v:
                    ckeys_mainwords.setdefault(key, []).append(k)
                    ckeys_mainwords_list.append(k)
        single_mainwords = list(set(self.param4_fre.keys()) - set(ckeys_mainwords_list))
        return ckeys_mainwords, single_mainwords

    def De_duplication(self, ckeys_mainwords):
        keys = list(ckeys_mainwords.keys())      # 修改 2022-5-8 原有错误：①先入为主，比较的四种情况；②顺序叠加，集合关系不应考虑顺序
        all_main_words = list(ckeys_mainwords.values())
        del_index = []
        for i, main_words in enumerate(all_main_words):
            score = 0
            for j, next_words in enumerate(all_main_words):
                scoreN = 0
                if i in del_index: break
                elif i == j or j in del_index: continue
                if main_words in next_words or main_words == next_words:
                    for word in main_words:
                        score += self.fres[word][keys[i]]
                    for word in next_words:
                        scoreN += self.fres[word][keys[j]]
                    if score <= scoreN:
                        print("有冲突的是", keys[i], "和", keys[j])
                        del_index.append(i)
                    else:
                        del_index.append(j)
        del_keys = [keys[i] for i in del_index]
        for k in del_keys:
            del ckeys_mainwords[k]

        # dup = {}
        # new_ckeys_mainwords = {}
        # for key, main_words in ckeys_mainwords.items():
        #     str = ''
        #     score = 0
        #     for word in main_words:
        #         str+= word
        #         score += self.fres[word][key]
        #     judge = True                                 # 重要修改 2021-12-29（只考虑了三种比较）
        #     for dk in list(dup.keys()):
        #         if str in dk and len(str) != len(dk):
        #             judge = False
        #             str = dk
        #             print("1有冲突的是", key, "和", dup[dk][0])
        #         if judge:
        #             if str not in dup:
        #                 new_ckeys_mainwords[key] = main_words
        #                 dup[str] = [key, score]
        #             else:
        #                 d = dup[str] if str in dup else 0
        #                 if score > float(d[1]):
        #                     print("2有冲突的是", key, "和", d[0])
        #                     new_ckeys_mainwords[key] = main_words
        #                     new_ckeys_mainwords.pop(d[0])
        #                     dup[str] = [key, score]
        # return new_ckeys_mainwords
        return ckeys_mainwords

    def Merge_synonyms_utils(self, new_ckeys_mainwords):
        mains = []
        for mainwords in new_ckeys_mainwords.values():
            mains.extend(mainwords)
        compete_mainwords = set([main for main in mains if mains.count(main) > 1])
        mainwords_ckeys_1_n = {}
        for main in compete_mainwords:
            for kw, mainwords in new_ckeys_mainwords.items():
                if main in mainwords:
                    mainwords_ckeys_1_n.setdefault(main, []).append(kw)
        return compete_mainwords, mainwords_ckeys_1_n

    def Compete_keywords_merge_synonyms(self, compete_mainwords, mainwords_ckeys_1_n, new_ckeys_mainwords):
        for mainw in compete_mainwords:
            repeat_list = mainwords_ckeys_1_n[mainw]
            max_fre = 0
            scores = 0
            max_key = ''
            for si in [s for s in self.fres[mainw].values()]:
                scores+=si
            for li in repeat_list:
                score = self.fres[mainw][li] / scores if li in self.fres[mainw] else 0
                if score > max_fre:  # 如果该实体所在的关键词词频大于最大值
                    max_fre = score  # 最大值设为该词频
                    max_key = str(li)  # 最大关键词设为该关键词
            for key2, value in new_ckeys_mainwords.items():  # 开始断开边
                if max_key != key2 and mainw in value:
                    wordsList = new_ckeys_mainwords[key2]
                    wordsList.remove(mainw)
                    new_ckeys_mainwords[key2] = wordsList
        return new_ckeys_mainwords

    def Merge_synonyms(self, new_ckeys_mainwords, single_mainwords):
        group = []
        for mainwords in new_ckeys_mainwords.values():
            if len(mainwords)>=1:
                group.append(list(mainwords))
        for mainword in single_mainwords:
            group.append([mainword])
        return group

    def switch(self):
        ckeys_mainwords, single_mainwords = self.Co_occurrence_keywords()
        new_ckeys_mainwords = self.De_duplication(ckeys_mainwords=ckeys_mainwords)
        compete_mainwords, mainwords_ckeys_1_n = self.Merge_synonyms_utils(new_ckeys_mainwords=new_ckeys_mainwords)
        new_ckeys_mainwords = self.Compete_keywords_merge_synonyms(compete_mainwords=compete_mainwords,
                                                                 mainwords_ckeys_1_n=mainwords_ckeys_1_n,
                                                                 new_ckeys_mainwords=new_ckeys_mainwords)
        group = self.Merge_synonyms(new_ckeys_mainwords=new_ckeys_mainwords, single_mainwords=single_mainwords)
        return group

# 预处理
def preprocessing(documents, stopP):
    all, entities = separate(documents=documents)
    all = filter_stopwords(stopP, all=all)
    entities, all = distinct(all, entities)
    document = [" ".join(sent0) for sent0 in all]
    return document, entities

if __name__ == '__main__':
    start = time.time()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'data', 'canopy聚类文档(0.8,0.86).txt')
    stopP = os.path.join(dir_path, 'data', '哈工大停用词表.txt')
    docs = readDict(path)
    print("开始构建类簇关键词词频矩阵……")
    # 预处理
    document, entities = preprocessing(documents=docs, stopP=stopP)
    print("构建完成")
    print("未聚类前，有%d个类簇" % len(entities))
    print("开始迭代执行相织算法")
    # 相织算法
    last_group = []
    ms = Merge_synonyms(dataset=document, entities=entities)
    group = ms.switch()
    num = 1
    clusters = 0
    print("第%d次聚类的簇数为%d" % (num, len(group)))
    # 再生成docs
    while True:
        resultsP = os.path.join(dir_path, 'data', '第%d次结果.txt'%(num))
        if clusters == len(group):
            print("KeyWords算法执行了%d次" % num)
            break
        else:
            clusters = len(group)
        if num == 1:
            last_group = group
        else:
            for i, gro in enumerate(group):
                new_gro = []
                for w in gro:
                   new_gro.extend([g for lg in last_group for g in lg if w in lg])
                group[i] = new_gro
            last_group = group
        writeJson(data=group, path=resultsP)
        num+=1
        groupD = {}
        for gro in group:
            docu = []
            kw = gro[-1]
            for mainword in gro:
                D = docs[mainword]
                docu.extend(D)
            groupD[kw] = docu
        document, entities = preprocessing(groupD, stopP=stopP)


        merge = Merge_synonyms(dataset=document, entities=entities)
        group = merge.switch()
        print("第%d次聚类的簇数为%d" % (num, len(group)))
    print("相织算法执行结束！")

