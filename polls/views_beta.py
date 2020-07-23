# from django.shortcuts import render
#
# # Create your views here.


from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Like
import pandas as pd
import os
import numpy as np
from random import seed, randint

from polls.search import searchByKeyword, findSimilarTopic

pre = os.path.dirname(os.path.realpath(__file__))

# First Call : Pavilion
excel_file = 'IROS2020_onDemand.xlsx'
path1 = os.path.join(pre, excel_file)
Cartegories = pd.read_excel(path1, sheet_name=0)

excel_file3 = 'ICRA20Digest4369_1.xlsx'
path3 = os.path.join(pre, excel_file3)
icra_example = pd.read_excel(path3, sheet_name=0)
icra_example = icra_example.fillna('missing')

# Monday Session
icra_Monday = icra_example[(icra_example['SchCode'].str[0] == 'M') & (icra_example['SchCode'].str[1] == 'o')]
icra_sessiontitle = icra_Monday['Session title']

Pavilion1 = icra_Monday[(icra_Monday['Session title'] == 'Aerial Systems - Applications I')
                        | (icra_Monday['Session title'] == 'Marine Robotics I')
                        | (icra_Monday['Session title'] == 'Marine Robotics II')
                        | (icra_Monday['Session title'] == 'Marine Robotics III')
                        | (icra_Monday['Session title'] == 'Aerial Systems - Applications II')
                        | (icra_Monday['Session title'] == 'Aerial Systems - Applications III')
                        | (icra_Monday['Session title'] == 'Field and Space Robots')]
Pavilion2 = icra_Monday[(icra_Monday['Session title'] == 'Legged Robots I')
                        | (icra_Monday['Session title'] == 'Prosthetics and Exoskeletons I')
                        | (icra_Monday['Session title'] == 'Legged Robots II')
                        | (icra_Monday['Session title'] == 'Legged Robots III')
                        | (icra_Monday['Session title'] == 'Prosthetics and Exoskeletons II')
                        | (icra_Monday['Session title'] == 'Prosthetics and Exoskeletons III')
                        | (icra_Monday['Session title'] == 'Legged Robots IV')]
Pavilion3 = icra_Monday[(icra_Monday['Session title'] == 'Surgical Robotics - Laparascopy I')
                        | (icra_Monday['Session title'] == 'Surgical Robotics - Laparoscopy II')
                        | (icra_Monday['Session title'] == 'Surgical Robotics - Steerable Catheters and Needles')
                        | (icra_Monday['Session title'] == 'Biological Cell Manipulation')
                        | (icra_Monday['Session title'] == 'Brain-Machine Interfaces')]
Pavilion4 = icra_Monday[(icra_Monday['Session title'] == 'Autonomous Driving I')
                        | (icra_Monday['Session title'] == 'Autonomous Driving II')
                        | (icra_Monday['Session title'] == 'Autonomous Driving III')
                        | (icra_Monday['Session title'] == 'Service Robots')
                        | (icra_Monday['Session title'] == 'Agricultural Automation')
                        | (icra_Monday['Session title'] == 'Autonomous Driving IV')]
Pavilion5 = icra_Monday[(icra_Monday['Session title'] == 'Grasping I')
                        | (icra_Monday['Session title'] == 'Grasping II')
                        | (icra_Monday['Session title'] == 'Grasping III')
                        | (icra_Monday['Session title'] == 'Grasping IV')
                        | (icra_Monday['Session title'] == 'Force and Tactile Sensing I')
                        | (icra_Monday['Session title'] == 'Force and Tactile Sensing II')
                        | (icra_Monday['Session title'] == 'Force and Tactile Sensing III')
                        | (icra_Monday['Session title'] == 'Force and Tactile Sensing IV')]
Sessions1 = sorted(list(set(Pavilion1['Session title'])))
Sessions2 = sorted(list(set(Pavilion2['Session title'])))
Sessions3 = sorted(list(set(Pavilion3['Session title'])))
Sessions4 = sorted(list(set(Pavilion4['Session title'])))
Sessions5 = sorted(list(set(Pavilion5['Session title'])))


# print(icra_example[(icra_example['Nr'] == 2375)])
def main(request):
    # for p in Like.objects.raw('SELECT * FROM polls_like'):
    #     print(p)
    # #
    # like = Like(name="user_id", paper_id="paper_id")
    # like.save()

    return render(request, './beta/practiceICRA_beta.html',
                  {'Pavilion': Cartegories['Pavilion'],
                   'Aerial': Sessions1,
                   'Humanoid': Sessions2,
                   'Medical': Sessions3,
                   'Driverless': Sessions4,
                   'EndEffector': Sessions5
                   })


def tvshow(request):
    selectedSession = request.GET['id']
    selectedPavilion = request.GET['id2']
    selectedPavilionNum = request.GET['id3']

    if selectedPavilion == Cartegories['Pavilion'][0]:
        selectedSessionList = Sessions1
    elif selectedPavilion == Cartegories['Pavilion'][1]:
        selectedSessionList = Sessions2
    elif selectedPavilion == Cartegories['Pavilion'][2]:
        selectedSessionList = Sessions3
    elif selectedPavilion == Cartegories['Pavilion'][3]:
        selectedSessionList = Sessions4
    elif selectedPavilion == Cartegories['Pavilion'][4]:
        selectedSessionList = Sessions5
    else:
        selectedSessionList = []

    EpisodeList = icra_Monday[(icra_Monday['Session title'] == selectedSession)]
    AuthorList1 = EpisodeList['Author1'].reset_index()
    AuthorList2 = EpisodeList['Author2'].reset_index()
    AuthorList3 = EpisodeList['Author3'].reset_index()
    AuthorList4 = EpisodeList['Author4'].reset_index()
    AuthorList5 = EpisodeList['Author5'].reset_index()
    AuthorList6 = EpisodeList['Author6'].reset_index()
    AffiliationList1 = EpisodeList['Affiliation1'].reset_index()
    AffiliationList2 = EpisodeList['Affiliation2'].reset_index()
    AffiliationList3 = EpisodeList['Affiliation3'].reset_index()
    AffiliationList4 = EpisodeList['Affiliation4'].reset_index()
    AffiliationList5 = EpisodeList['Affiliation5'].reset_index()

    TitleList = EpisodeList['Title'].reset_index()
    PDFList = EpisodeList['FN'].reset_index()
    titleNumber = EpisodeList['Nr'].reset_index()
    EpisodeContext = zip(AuthorList1['Author1'], AuthorList2['Author2'],
                         AuthorList3['Author3'],
                         AuthorList4['Author4'],
                         AuthorList5['Author5'],
                         AuthorList6['Author6'],
                         AffiliationList1['Affiliation1'],
                         AffiliationList2['Affiliation2'],
                         AffiliationList3['Affiliation3'],
                         AffiliationList4['Affiliation4'],
                         AffiliationList5['Affiliation5'],
                         TitleList['Title'],
                         PDFList['FN'], titleNumber['Nr'])
    EpisodeCount = EpisodeList.shape[0] + 1
    # print(titleNumber)

    return render(request, './beta/practiceICRA2_beta.html', {'Pavilion': selectedPavilion,
                                                  'PavilionNum': selectedPavilionNum,
                                                  'SessionList': selectedSessionList,
                                                  'Session': selectedSession,
                                                  'EpisodeContext': EpisodeContext,
                                                  'EpisodeCount': range(1, EpisodeCount)
                                                  })


def episode(request):
    selectedTitle = request.GET['id']
    findVideo = icra_example[(icra_example['Title'] == selectedTitle)]
    VideoList = findVideo['VID'].reset_index()
    selectedNumber = findVideo['Nr'].reset_index()
    suggestEpisodeNum = findSimilarTopic(selectedNumber['Nr'].iloc[0])

    similarPaper = icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[0]))]

    for i in range(1, 12):
        main2 = similarPaper.append(icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[i]))])
        similarPaper = main2

    AuthorList1 = similarPaper['Author1'].reset_index()
    AuthorList2 = similarPaper['Author2'].reset_index()
    AuthorList3 = similarPaper['Author3'].reset_index()
    AuthorList4 = similarPaper['Author4'].reset_index()
    AuthorList5 = similarPaper['Author5'].reset_index()
    AuthorList6 = similarPaper['Author6'].reset_index()
    AffiliationList1 = similarPaper['Affiliation1'].reset_index()
    AffiliationList2 = similarPaper['Affiliation2'].reset_index()
    AffiliationList3 = similarPaper['Affiliation3'].reset_index()
    AffiliationList4 = similarPaper['Affiliation4'].reset_index()
    AffiliationList5 = similarPaper['Affiliation5'].reset_index()

    TitleList = similarPaper['Title'].reset_index()
    PDFList = similarPaper['FN'].reset_index()
    titleNumber = similarPaper['Nr'].reset_index()
    resultList = zip(AuthorList1['Author1'], AuthorList2['Author2'],
                     AuthorList3['Author3'],
                     AuthorList4['Author4'],
                     AuthorList5['Author5'],
                     AuthorList6['Author6'],
                     AffiliationList1['Affiliation1'],
                     AffiliationList2['Affiliation2'],
                     AffiliationList3['Affiliation3'],
                     AffiliationList4['Affiliation4'],
                     AffiliationList5['Affiliation5'],
                     TitleList['Title'],
                     PDFList['FN'], titleNumber['Nr'], suggestEpisodeNum)

    return render(request, './beta/practiceICRA3_beta.html', {'VideoList': VideoList['VID'],
                                                  'Title': selectedTitle,
                                                  'EpisodeContext': resultList,
                                                  'SelectedNumber': selectedNumber['Nr'].iloc[0]})


def suggestion(request):
    suggestedNum = request.GET['id1']
    findTitle = icra_example[(icra_example['Nr'] == int(suggestedNum))]
    titleName = findTitle['Title'].reset_index()
    VideoList = findTitle['VID'].reset_index()
    selectedTitle = titleName['Title'].iloc[0]
    suggestEpisodeNum = findSimilarTopic(int(suggestedNum))

    suggestPaper = icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[0]))]

    for i in range(1, 12):
        main2 = suggestPaper.append(icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[i]))])
        suggestPaper = main2

    AuthorList1 = suggestPaper['Author1'].reset_index()
    AuthorList2 = suggestPaper['Author2'].reset_index()
    AuthorList3 = suggestPaper['Author3'].reset_index()
    AuthorList4 = suggestPaper['Author4'].reset_index()
    AuthorList5 = suggestPaper['Author5'].reset_index()
    AuthorList6 = suggestPaper['Author6'].reset_index()
    AffiliationList1 = suggestPaper['Affiliation1'].reset_index()
    AffiliationList2 = suggestPaper['Affiliation2'].reset_index()
    AffiliationList3 = suggestPaper['Affiliation3'].reset_index()
    AffiliationList4 = suggestPaper['Affiliation4'].reset_index()
    AffiliationList5 = suggestPaper['Affiliation5'].reset_index()

    TitleList = suggestPaper['Title'].reset_index()
    PDFList = suggestPaper['FN'].reset_index()
    titleNumber = suggestPaper['Nr'].reset_index()
    resultList = zip(AuthorList1['Author1'], AuthorList2['Author2'],
                     AuthorList3['Author3'],
                     AuthorList4['Author4'],
                     AuthorList5['Author5'],
                     AuthorList6['Author6'],
                     AffiliationList1['Affiliation1'],
                     AffiliationList2['Affiliation2'],
                     AffiliationList3['Affiliation3'],
                     AffiliationList4['Affiliation4'],
                     AffiliationList5['Affiliation5'],
                     TitleList['Title'],
                     PDFList['FN'], titleNumber['Nr'], suggestEpisodeNum)

    return render(request, './beta/practiceICRA3_beta.html', {'VideoList': VideoList['VID'],
                                                  'Title': selectedTitle,
                                                  'EpisodeContext': resultList})


def searchresult(request):
    inputKeyword = request.GET['id']
    # print(inputKeyword)
    resultNumber = searchByKeyword(inputKeyword)
    resultNumberlength = len(resultNumber)

    if not resultNumber:
        return render(request, './beta/practiceICRA5_beta.html', {'inputKeyword': inputKeyword})
    else:
        searchTitle = icra_example[(icra_example['Nr'] == int(resultNumber[0]))]

        for i in range(1, resultNumberlength):
            main2 = searchTitle.append(icra_example[(icra_example['Nr'] == int(resultNumber[i]))])
            # print(main2)
            searchTitle = main2

        # print(searchTitle)

        AuthorList1 = searchTitle['Author1'].reset_index()
        AuthorList2 = searchTitle['Author2'].reset_index()
        AuthorList3 = searchTitle['Author3'].reset_index()
        AuthorList4 = searchTitle['Author4'].reset_index()
        AuthorList5 = searchTitle['Author5'].reset_index()
        AuthorList6 = searchTitle['Author6'].reset_index()
        AffiliationList1 = searchTitle['Affiliation1'].reset_index()
        AffiliationList2 = searchTitle['Affiliation2'].reset_index()
        AffiliationList3 = searchTitle['Affiliation3'].reset_index()
        AffiliationList4 = searchTitle['Affiliation4'].reset_index()
        AffiliationList5 = searchTitle['Affiliation5'].reset_index()
        TitleList = searchTitle['Title'].reset_index()
        PDFList = searchTitle['FN'].reset_index()
        titleNumber = searchTitle['Nr'].reset_index()
        resultList = zip(AuthorList1['Author1'], AuthorList2['Author2'],
                         AuthorList3['Author3'],
                         AuthorList4['Author4'],
                         AuthorList5['Author5'],
                         AuthorList6['Author6'],
                         AffiliationList1['Affiliation1'],
                         AffiliationList2['Affiliation2'],
                         AffiliationList3['Affiliation3'],
                         AffiliationList4['Affiliation4'],
                         AffiliationList5['Affiliation5'],
                         TitleList['Title'],
                         PDFList['FN'], titleNumber['Nr'])
        return render(request, './beta/practiceICRA4_beta.html', {'EpisodeContext': resultList})
