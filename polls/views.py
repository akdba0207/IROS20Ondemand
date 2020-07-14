# from django.shortcuts import render
#
# # Create your views here.


from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import openpyxl
import os

pre = os.path.dirname(os.path.realpath(__file__))

# First Call : Pavilion
excel_file = 'IROS2020_onDemand.xlsx'
path1 = os.path.join(pre, excel_file)
Cartegories = pd.read_excel(path1, sheet_name=0)

excel_file3 = 'ICRA20Digest4369_1.xlsx'
path3 = os.path.join(pre, excel_file3)
icra_example = pd.read_excel(path3,sheet_name=0)

#Monday Session
icra_Monday = icra_example[(icra_example['SchCode'].str[0]=='M')&(icra_example['SchCode'].str[1]=='o')]
icra_sessiontitle= icra_Monday['Session title']

Pavilion1 = icra_Monday[(icra_Monday['Session title']=='Aerial Systems - Applications I')
                        |(icra_Monday['Session title']=='Marine Robotics I')
                        |(icra_Monday['Session title']=='Marine Robotics II')
                        |(icra_Monday['Session title']=='Marine Robotics III')
                        |(icra_Monday['Session title']=='Aerial Systems - Applications II')
                        |(icra_Monday['Session title']=='Aerial Systems - Applications III')
                        |(icra_Monday['Session title']=='Field and Space Robots')]
Pavilion2 = icra_Monday[(icra_Monday['Session title']=='Legged Robots I')
                        |(icra_Monday['Session title']=='Prosthetics and Exoskeletons I')
                        |(icra_Monday['Session title']=='Legged Robots II')
                        |(icra_Monday['Session title']=='Legged Robots III')
                        |(icra_Monday['Session title']=='Prosthetics and Exoskeletons II')
                        |(icra_Monday['Session title']=='Prosthetics and Exoskeletons III')
                        |(icra_Monday['Session title']=='Legged Robots IV')]
Pavilion3 = icra_Monday[(icra_Monday['Session title']=='Surgical Robotics - Laparascopy I')
                        |(icra_Monday['Session title']=='Surgical Robotics - Laparoscopy II')
                        |(icra_Monday['Session title']=='Surgical Robotics - Steerable Catheters&Needles')
                        |(icra_Monday['Session title']=='Biological Cell Manipulation')
                        |(icra_Monday['Session title']=='Brain-Machine Interfaces')]
Pavilion4 = icra_Monday[(icra_Monday['Session title']=='Autonomous Driving I')
                        |(icra_Monday['Session title']=='Autonomous Driving II')
                        |(icra_Monday['Session title']=='Autonomous Driving III')
                        |(icra_Monday['Session title']=='Service Robots')
                        |(icra_Monday['Session title']=='Agricultural Automation')
                        |(icra_Monday['Session title']=='Autonomous Driving IV')]
Pavilion5 = icra_Monday[(icra_Monday['Session title']=='Grasping I')
                        |(icra_Monday['Session title']=='Grasping II')
                        |(icra_Monday['Session title']=='Grasping III')
                        |(icra_Monday['Session title']=='Grasping IV')
                        |(icra_Monday['Session title']=='Force and Tactile Sensing I')
                        |(icra_Monday['Session title']=='Force and Tactile Sensing II')
                        |(icra_Monday['Session title']=='Force and Tactile Sensing III')
                        |(icra_Monday['Session title']=='Force and Tactile Sensing IV')]
Sessions1 = sorted(list(set(Pavilion1['Session title'])))
Sessions2 = sorted(list(set(Pavilion2['Session title'])))
Sessions3 = sorted(list(set(Pavilion3['Session title'])))
Sessions4 = sorted(list(set(Pavilion4['Session title'])))
Sessions5 = sorted(list(set(Pavilion5['Session title'])))

def main(request):

    return render(request, 'practiceICRA.html',
                  {'Pavilion': Cartegories['Pavilion'],
                   'Aerial': Sessions1,
                   'Humanoid': Sessions2,
                   'Medical': Sessions3,
                   'Driverless': Sessions4,
                   'EndEffector': Sessions5})

def tvshow(request):
    selectedSession = request.GET['id']
    selectedPavilion = request.GET['id2']
    selectedPavilionNum = request.GET['id3']

    if selectedPavilion ==Cartegories['Pavilion'][0]:
        selectedSessionList = Sessions1
    elif selectedPavilion ==Cartegories['Pavilion'][1]:
        selectedSessionList = Sessions2
    elif selectedPavilion ==Cartegories['Pavilion'][2]:
        selectedSessionList = Sessions3
    elif selectedPavilion ==Cartegories['Pavilion'][3]:
        selectedSessionList = Sessions4
    elif selectedPavilion ==Cartegories['Pavilion'][4]:
        selectedSessionList = Sessions5
    else:
        selectedSessionList = []

    EpisodeList = icra_Monday[(icra_Monday['Session title']==selectedSession)]
    AuthorList = EpisodeList['Author1'].reset_index()
    AffiliationList = EpisodeList['Affiliation1'].reset_index()
    TitleList = EpisodeList['Title'].reset_index()
    PDFList = EpisodeList['FN'].reset_index()
    EpisodeContext = zip(AuthorList['Author1'],AffiliationList['Affiliation1'],TitleList['Title'],
                         PDFList['FN'])
    EpisodeCount = EpisodeList.shape[0]+1

    return render(request, 'practiceICRA2.html', {'Pavilion': selectedPavilion,
                                                  'PavilionNum': selectedPavilionNum,
                                                  'SessionList':selectedSessionList,
                                                  'Session': selectedSession,
                                                  'EpisodeContext':EpisodeContext,
                                                  'EpisodeCount':range(1, EpisodeCount)})

def episode(request):
    selectedTitle = request.GET['id']
    findVideo = icra_Monday[(icra_Monday['Title']==selectedTitle)]
    VideoList = findVideo['VID'].reset_index()
    print(VideoList)
    return render(request, 'practiceICRA3.html', {'VideoList': VideoList['VID'],
                                                  'Title':selectedTitle})
