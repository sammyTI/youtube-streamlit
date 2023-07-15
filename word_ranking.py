# f = open('scraping_otocre.txt', encoding='utf-8')
# text = f.read()  # ファイル終端まで全て読んだデータを返す
# f.close()
# # print(text)

# #MeCabで分割
# import MeCab
# m = MeCab.Tagger ('-Ochasen')
 
# node = m.parseToNode(text)
# words=[]
# while node:
#     hinshi = node.feature.split(",")[0]
#     if hinshi in ["名詞","動詞","形容詞"]:
#         origin = node.feature.split(",")[6]
#         words.append(origin)
#     node = node.next
# # print(words)

# #単語の数カウント
# import collections
# c = collections.Counter(words)
# print(c.most_common(20))



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import MeCab as mc
from collections import Counter

# 1.mecabを用いて単語に分けます。
def mecab_analysis(text):
    t = mc.Tagger("-Ochasen")
    t.parse('')
    node = t.parseToNode(text) 
    output = []
    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            # if word_type in ["形容詞", "動詞","名詞", "副詞"]:
            if word_type in ["名詞","動詞","形容詞"]:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output

def count_csv():
    text= str(open('scraping_otocre.txt', encoding='utf-8').read())
    words = mecab_analysis(text)
# 2.集計して
    counter = Counter(words)
# 3.出力します
    for word, count in counter.most_common():
        if len(word) > 0 and count > 1:

            print ("%s,%d" % (word, count))

def main():
    count_csv()

if __name__ == '__main__':
   main()
