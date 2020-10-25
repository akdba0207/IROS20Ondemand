import re

import nltk
from django.shortcuts import render
import pandas as pd

import os
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

pre = os.path.dirname(os.path.realpath(__file__))

path3 = os.path.join(pre, 'IROS20_OnDemand__10_05_main.xlsx')
data = pd.read_excel(path3, sheet_name=0)
# data1 = pd.read_excel(path3, sheet_name=0)
# data = data1[(data1['SchCode'].str[0]=='M')&(data1['SchCode'].str[1]=='o')]
data = data.fillna('z')
data = data.iloc[0:1445,:]

# Call Workshops and Tutorials
excel_file4 = 'IROS20_WSandTR.xlsx'
path4 = os.path.join(pre, excel_file4)
iros_wstr = pd.read_excel(path4, sheet_name=0)
iros_wstr = iros_wstr.fillna('z')

def searchByKeyword(keyword, n_count=12):

    key = str.split(keyword.lower())
    scores = {}
    for c in key:
        ret = data[(data['Session title'].str.lower().str.find(c) >= 0) |
                   (data['Title'].str.lower().str.find(c) >= 0) |
                   (data['Author1'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation1'].str.lower().str.find(c) >= 0) |
                   (data['Author2'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation2'].str.lower().str.find(c) >= 0) |
                   (data['Author3'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation3'].str.lower().str.find(c) >= 0) |
                   (data['Author4'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation4'].str.lower().str.find(c) >= 0) |
                   (data['Author5'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation5'].str.lower().str.find(c) >= 0) |
                   (data['Author6'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation6'].str.lower().str.find(c) >= 0) |
                   (data['Author7'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation7'].str.lower().str.find(c) >= 0) |
                   (data['Author8'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation8'].str.lower().str.find(c) >= 0) |
                   (data['Author9'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation9'].str.lower().str.find(c) >= 0) |
                   (data['Author10'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation10'].str.lower().str.find(c) >= 0) |
                   (data['Author11'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation11'].str.lower().str.find(c) >= 0) |
                   (data['Author12'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation12'].str.lower().str.find(c) >= 0) |
                   (data['Author13'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation13'].str.lower().str.find(c) >= 0) |
                   (data['Author14'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation14'].str.lower().str.find(c) >= 0) |
                   (data['Author15'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation15'].str.lower().str.find(c) >= 0) |
                   (data['Author16'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation16'].str.lower().str.find(c) >= 0) |
                   (data['Author17'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation17'].str.lower().str.find(c) >= 0) |
                   (data['Author18'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation18'].str.lower().str.find(c) >= 0) |
                   (data['Author19'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation19'].str.lower().str.find(c) >= 0) |
                   (data['Author20'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation20'].str.lower().str.find(c) >= 0) |
                   (data['Author21'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation21'].str.lower().str.find(c) >= 0) |
                   (data['Author22'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation22'].str.lower().str.find(c) >= 0) |
                   (data['Author23'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation23'].str.lower().str.find(c) >= 0) |
                   (data['Author24'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation24'].str.lower().str.find(c) >= 0) |
                   (data['Author25'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation25'].str.lower().str.find(c) >= 0) |
                   (data['Author26'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation26'].str.lower().str.find(c) >= 0) |
                   (data['Author27'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation27'].str.lower().str.find(c) >= 0) |
                   (data['Author28'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation28'].str.lower().str.find(c) >= 0) |
                   (data['Author29'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation29'].str.lower().str.find(c) >= 0) |
                   (data['Author30'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation30'].str.lower().str.find(c) >= 0) |
                   (data['Author31'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation31'].str.lower().str.find(c) >= 0) |
                   (data['Author32'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation32'].str.lower().str.find(c) >= 0) |
                   (data['Author33'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation33'].str.lower().str.find(c) >= 0) |
                   (data['Author34'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation34'].str.lower().str.find(c) >= 0) |
                   (data['Author35'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation35'].str.lower().str.find(c) >= 0) |
                   (data['Author36'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation36'].str.lower().str.find(c) >= 0) |
                   (data['Author37'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation37'].str.lower().str.find(c) >= 0) |
                   (data['Author38'].str.lower().str.find(c) >= 0) |
                   (data['Affiliation38'].str.lower().str.find(c) >= 0) |
                   (data['Keyword1'].str.lower().str.find(c) >= 0) |
                   (data['Keyword2'].str.lower().str.find(c) >= 0) |
                   (data['Keyword3'].str.lower().str.find(c) >= 0)]

        for _, r in ret.iterrows():
            if r['Nr'] in scores:
                scores[r['Nr']] += 1
            else:
                scores[r['Nr']] = 1

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores = [k for k, _ in scores[0:n_count]]
    return scores

def searchWSByKeyword(keyword, n_count=12):

    key = str.split(keyword.lower())
    scores = {}
    for c in key:
        ret = iros_wstr[(iros_wstr['Workshop Title'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['WS/TR Nr'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Title'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Speaker'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Institution'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Workshop Abstract'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer1'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer1Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer2'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer2Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer3'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer3Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer4'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer4Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer5'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer5Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer6'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer6Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer7'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer7Affil'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer8'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer8Affil'].str.lower().str.find(c) >= 0)|
                        (iros_wstr['Organizer9'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer9Affil'].str.lower().str.find(c) >= 0)|
                        (iros_wstr['Organizer10'].str.lower().str.find(c) >= 0) |
                        (iros_wstr['Organizer10Affil'].str.lower().str.find(c) >= 0)]

        for _, r in ret.iterrows():
            if r['Nr'] in scores:
                scores[r['Nr']] += 1
            else:
                scores[r['Nr']] = 1

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores = [k for k, _ in scores[0:n_count]]
    return scores


def strip_suffixes(s,suffixes):
    for suf in suffixes:
        if s.endswith(suf):
            return s.rstrip(suf)
    return s
def findSimilarTopic(index, n_count=12):

    obj = data[(data['Nr'] == index)].iloc[0]

    keyword = obj['Keyword1'] + " " + obj['Keyword2'] + " " + obj['Keyword2'] + " " + obj['Keyword3'] + " " + obj[
        'Title']
    s_title = obj['Session title']
    key = str.split(keyword)

    pos_tagged = nltk.pos_tag(key)
    f = filter(lambda x: x[1] != 'IN' and x[1] != 'CC' and x[0].lower() != 'using'
               , pos_tagged)

    key = set([strip_suffixes(re.sub('\W+', '', k[0]), ['s', 'es']) for k in f])

    scores = {}
    for c in key:
        ret = data[(((data['Title'].str.find(c) >= 0) |
                     (data['Keyword1'].str.find(c) >= 0) |
                     (data['Keyword2'].str.find(c) >= 0) |
                     (data['Keyword3'].str.find(c) >= 0)) &
                    (data['Nr'] != index))]

        for _, r in ret.iterrows():

            if s_title == data['Session title'].str:
                scores[r['Nr']] += 1

            if r['Nr'] in scores:
                scores[r['Nr']] += 1
            else:
                scores[r['Nr']] = 1

    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #print(scores)
    scores = [k for k, _ in scores[0:n_count]]

    return scores
