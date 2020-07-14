import nltk
from django.shortcuts import render
import pandas as pd

import os
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

pre = os.path.dirname(os.path.realpath(__file__))

path3 = os.path.join(pre, 'ICRA20Digest4369_1.xlsx')
data = pd.read_excel(path3, sheet_name=0)


def searchByKeyword(keyword):
    ret = data[(data['Session title'].str.find(keyword) >= 0) |
               (data['Title'].str.find(keyword) >= 0) |
               (data['Author1'].str.find(keyword) >= 0) |
               (data['Affiliation1'].str.find(keyword) >= 0) |
               (data['Author2'].str.find(keyword) >= 0) |
               (data['Affiliation2'].str.find(keyword) >= 0) |
               (data['Author3'].str.find(keyword) >= 0) |
               (data['Affiliation3'].str.find(keyword) >= 0) |
               (data['Author4'].str.find(keyword) >= 0) |
               (data['Affiliation4'].str.find(keyword) >= 0) |
               (data['Author5'].str.find(keyword) >= 0) |
               (data['Affiliation5'].str.find(keyword) >= 0)
               ]
    return ret


def findSimilarTopic(index, n_count=20):
    obj = data[(data['Nr'] == index)].iloc[0]
    title = obj['Title']
    s_title = obj['Session title']

    key = str.split(title)

    pos_tagged = nltk.pos_tag(key)
    f = filter(lambda x: x[1] != 'IN' and x[1] != 'CC'
               , pos_tagged)

    key = [k[0] for k in f]

    scores = {}
    for c in key:
        ret = data[((data['Title'].str.find(c) >= 0) &
                    (data['Nr'] != index))]

        for _, r in ret.iterrows():

            if s_title == data['Session title'].str:
                scores[r['Nr']] += 1

            if r['Nr'] in scores:
                scores[r['Nr']] += 1
            else:
                scores[r['Nr']] = 1

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # scores = [k for k, _ in scores[0:n_count]]

    return scores


