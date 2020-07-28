# from django.shortcuts import render
#
# # Create your views here.


from django.http import HttpResponse
from django.shortcuts import render
from polls.models import Like, ieeeusers, iros2020registered
import pandas as pd
import os
import numpy as np

from polls.search import searchByKeyword, findSimilarTopic

#IROS2020 Registered List
iros2020registered_email=[]
iros2020registered_name=[]
mydict = dict()

for p in iros2020registered.objects.raw('SELECT * FROM polls_iros2020registered'):
    iros2020registered_email.append(p.iros2020_email)
    iros2020registered_name.append(p.iros2020_name)
    mydict[p.iros2020_email] = p.iros2020_name

iros2020registered_email = sorted(iros2020registered_email)

pre = os.path.dirname(os.path.realpath(__file__))

# Call Genres, Pavilion
excel_file1 = 'IROS2020_onDemand_beta.xlsx'
path1 = os.path.join(pre, excel_file1)
Cartegories = pd.read_excel(path1, sheet_name=0)

excel_file2 = 'ICRA20Digest4369_1.xlsx'
path2 = os.path.join(pre, excel_file2)
icra_example = pd.read_excel(path2, sheet_name=0)
icra_example = icra_example.fillna('missing')

# Call Keynotes and Plenaries
excel_file3 = 'ICRA20KeynotesandPlenaries.xlsx'
path3 = os.path.join(pre, excel_file3)
icra_specials = pd.read_excel(path3, sheet_name=0)

# Call Workshops and Tutorials
excel_file4 = 'ICRA2020Workshops.xlsx'
path4 = os.path.join(pre,excel_file4)
icra_workshops = pd.read_excel(path4, sheet_name=0)
icra_workshops = icra_workshops.fillna('missing')

# Call Sponsors
excel_file6 = 'ICRA20Sponsors.xlsx'
path6 = os.path.join(pre,excel_file6)
icra_sponsors = pd.read_excel(path6, sheet_name=0)
icra_sponsors = icra_sponsors.fillna('missing')


# Pavilion Monday Session
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

# Specials
Specials = icra_specials[(icra_specials['Genre']=='Plenaries')
                         |(icra_specials['Genre']=='Keynotes')]
SpecialsSession = sorted(list(set(Specials['Genre'])))


#Workshops
Workshops = icra_workshops[(icra_workshops['Workshop Number']==4)|
                           (icra_workshops['Workshop Number']==8)|
                           (icra_workshops['Workshop Number']==9)|
                           (icra_workshops['Workshop Number']==14)]

WorkshopsSession = sorted(list(set(Workshops['Title'])))
#########################################################################################################
#########################################################################################################
#########################################################################################################
#Login
def login(request):


    # for users in ieeeusers.objects.raw('SELECT * FROM polls_ieeeusers'):
    #     dongbin = users.ieeeusers_id
    #     dongbin1.append(dongbin)

    # ieeeusers.objects.filter(ieeeusers_id='iros1').update(ieeeusers_password='gyuhozzang')
    # irosuser1 = iros2020registered(iros2020_name="Dongbin Kim", iros2020_email="dongbin.kim@unlv.edu")
    # irosuser2 = iros2020registered(iros2020_name="Dr. Paul Oh", iros2020_email="paul.oh@unlv.edu")
    # irosuser1.save()
    # irosuser2.save()
    # irosuser3 = iros2020registered(iros2020_name="Gyuho Lee", iros2020_email="leeg3@unlv.nevada.edu")
    # irosuser4 = iros2020registered(iros2020_name="Blake Hament", iros2020_email="blakehament@gmail.com")
    # irosuser3.save()
    # irosuser4.save()
    # for i in range(1554):
    #     icralike = Like(paperid=icra_example['Nr'][i])
    #     icralike.save()

    return render(request,'./beta/1_login_beta.html')

#TODO : receive login ID and Password, pass it to main.
#TODO : When the passcode is wrong, it displays false alarm, or goes to main pages


#########################################################################################################
#########################################################################################################
#########################################################################################################
#Main Page
def binarySearch(arr, l, r, x):
    # Check base case
    if r >= l:
        mid = l + (r - l) // 2
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
            # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        # Element is not present in the array
        return -1

def main(request):
    global iros2020_emailinput
    iros2020_emailinput = request.GET['id']

    result= binarySearch(iros2020registered_email, 0, len(iros2020registered_email) - 1, iros2020_emailinput)

    if result != -1:
        # iros2020registered_name[result]
        loginName = mydict[iros2020_emailinput]

        return render(request, './beta/2_main_beta.html',
                      {'Pavilion': Cartegories['Pavilion'],
                       'Genre': Cartegories['Genre'],
                       'Specials': SpecialsSession,
                       'Workshops': WorkshopsSession,
                       'Aerial': Sessions1,
                       'Humanoid': Sessions2,
                       'Medical': Sessions3,
                       'Driverless': Sessions4,
                       'EndEffector': Sessions5,
                       'account':iros2020_emailinput,
                       'loginName':loginName
                       })
    else:
        return render(request, './beta/1-1_loginError_beta.html')


#########################################################################################################
#########################################################################################################
#########################################################################################################
#Sessions : Pavilion, Specials, Workshops
def tvshow(request):
    selectedSession = request.GET['id']
    selectedPavilion = request.GET['id2']
    selectedPavilionNum = request.GET['id3']
    global iros2020_emailinput


    if selectedPavilion == Cartegories['Pavilion'][1]:
        selectedSessionList = Sessions1
    elif selectedPavilion == Cartegories['Pavilion'][2]:
        selectedSessionList = Sessions2
    elif selectedPavilion == Cartegories['Pavilion'][3]:
        selectedSessionList = Sessions3
    elif selectedPavilion == Cartegories['Pavilion'][4]:
        selectedSessionList = Sessions4
    elif selectedPavilion == Cartegories['Pavilion'][5]:
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

    #Gold Sponsor Video
    goldSponsorSession = icra_sponsors[(icra_sponsors['Location'] == selectedSession)].reset_index()
    goldSponsorName = goldSponsorSession['Name'].reset_index()
    goldSponsorVideo = goldSponsorSession['Video'].reset_index()

    return render(request, './beta/3_pavilionSession_beta.html', {'Pavilion': selectedPavilion,
                                                                  'PavilionNum': selectedPavilionNum,
                                                                  'SessionList': selectedSessionList,
                                                                  'Session': selectedSession,
                                                                  'EpisodeContext': EpisodeContext,
                                                                  'EpisodeCount': range(1, EpisodeCount),
                                                                  'account':iros2020_emailinput,
                                                                  'goldSponsorName':goldSponsorName['Name'],
                                                                  'goldSponsorVideo':goldSponsorVideo['Video'],
                                                                  'goldSponsorSession':goldSponsorSession['Location']})
def specials(request):
    selectedSpecial = request.GET['id']
    selectedGenre = request.GET['id2']
    specialEpisodeList = icra_specials[(icra_specials['Genre']==selectedSpecial)]
    speakerName = specialEpisodeList['Speaker'].reset_index()
    speakerBiography = specialEpisodeList['Bio'].reset_index()
    specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
    specialEpisodeVideo = specialEpisodeList['Video'].reset_index()
    bioLength = []
    abstractLength = []
    for i in speakerBiography['Bio']:
        bioLength.append(len(i))
    for j in specialEpisodeAbstract['Abstract']:
        abstractLength.append(len(j))

    specialEpisodeContext = zip(speakerName['Speaker'],
                                speakerBiography['Bio'],
                                specialEpisodeAbstract['Abstract'],
                                bioLength,
                                abstractLength
                                )
    specialEpisodeCount = specialEpisodeList.shape[0]




    global iros2020_emailinput

    return render(request,'./beta/3-1_plenariesSession_beta.html',{'selectedSpecial':selectedSpecial,
                                                                   'selectedGenre':selectedGenre,
                                                                   'specialEpisodeContext':specialEpisodeContext,
                                                                   'SpecialsSession':SpecialsSession,
                                                                   'account':iros2020_emailinput,
                                                                   })

def workshops(request):
    selectedWorkshops = request.GET['id']
    selectedGenre = request.GET['id2']
    workshopsEpisodeList = icra_workshops[(icra_workshops['Title']==selectedWorkshops)].reset_index()
    workshopsHomepage = workshopsEpisodeList['Workshop Home Page'].iloc[0]
    workshopOrganizers = workshopsEpisodeList['Organizers'].iloc[0]
    global iros2020_emailinput

    Speaker = []
    for i in range(1,15):
        Speaker.append(workshopsEpisodeList['Speaker '+str(i)].iloc[0])

    Institution = []
    for j in range(1,15):
        Institution.append(workshopsEpisodeList['Institution '+str(j)].iloc[0])

    TalkTitle = []
    for k in range(1,15):
        TalkTitle.append(workshopsEpisodeList['Talk Title '+str(k)].iloc[0])

    WorkshopsContext = zip(Speaker, Institution, TalkTitle)


    return render(request,'./beta/3-2_workshopsSession_beta.html',{'selectedWorkshops':selectedWorkshops,
                                                                   'selectedGenre':selectedGenre,
                                                                   'WorkshopsContext':WorkshopsContext,
                                                                   'WorkshopsSession':WorkshopsSession,
                                                                   'workshopsHomepage':workshopsHomepage,
                                                                   'workshopOrganizers':workshopOrganizers,
                                                                   'account':iros2020_emailinput})



#########################################################################################################
#########################################################################################################
#########################################################################################################
#Episodes : Pavilion, Specials, Workshops
def episode(request):
    selectedTitle = request.GET['id']
    findVideo = icra_example[(icra_example['Title'] == selectedTitle)]
    VideoList = findVideo['VID'].reset_index()
    selectedNumber = findVideo['Nr'].reset_index()
    suggestEpisodeNum = findSimilarTopic(selectedNumber['Nr'].iloc[0])
    global iros2020_emailinput
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

    return render(request, './beta/4_pavilionSessionEpisode_beta.html', {'VideoList': VideoList['VID'],
                                                                         'Title': selectedTitle,
                                                                         'EpisodeContext': resultList,
                                                                         'SelectedNumber': selectedNumber['Nr'].iloc[0],
                                                                         'account':iros2020_emailinput})

def specialsepisode(request):
    selectedSpeaker=request.GET['id']
    selectedSpecial=request.GET['id2']
    selectedGenre=request.GET['id3']
    findspeaker=icra_specials[(icra_specials['Speaker']==selectedSpeaker)]
    specialVideo=findspeaker['Video'].reset_index()
    global iros2020_emailinput

    #Other Specials
    specialEpisodeList = icra_specials[(icra_specials['Genre'] == selectedSpecial)]
    speakerName = specialEpisodeList['Speaker'].reset_index()
    speakerBiography = specialEpisodeList['Bio'].reset_index()
    specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
    specialEpisodeContext = zip(speakerName['Speaker'],
                                speakerBiography['Bio'],
                                specialEpisodeAbstract['Abstract']
                                )
    print(specialVideo['Video'])
    return render(request,'./beta/4-1_plenariesSessionEpisode_beta.html',{'specialVideo':specialVideo['Video'],
                                                                          'selectedSpeaker':selectedSpeaker,
                                                                          'selectedSpecial':selectedSpecial,
                                                                          'selectedGenre':selectedGenre,
                                                                          'specialEpisodeContext':specialEpisodeContext,
                                                                          'account':iros2020_emailinput})


def workshopsepisode(request):
    selectedSpeaker = request.GET['id']
    selectedWorkshops = request.GET['id2']
    selectedGenre = request.GET['id3']
    selectedSpeakerNumber = request.GET['id4']
    print(selectedSpeakerNumber)
    findspeaker = icra_workshops[(icra_workshops['Speaker '+str(selectedSpeakerNumber)] == selectedSpeaker)]
    print(findspeaker)
    workshopsVideo = findspeaker['Video '+ str(selectedSpeakerNumber)].reset_index()
    print(workshopsVideo)
    workshopsTalkTitle = findspeaker['Talk Title ' + str(selectedSpeakerNumber)].reset_index()
    print(workshopsTalkTitle)
    #Other Workshops Talk
    workshopsEpisodeList = icra_workshops[(icra_workshops['Title'] == selectedWorkshops)].reset_index()
    global iros2020_emailinput

    Speaker = []
    for i in range(1, 15):
        Speaker.append(workshopsEpisodeList['Speaker ' + str(i)].iloc[0])

    Institution = []
    for j in range(1, 15):
        Institution.append(workshopsEpisodeList['Institution ' + str(j)].iloc[0])

    TalkTitle = []
    for k in range(1, 15):
        TalkTitle.append(workshopsEpisodeList['Talk Title ' + str(k)].iloc[0])

    WorkshopsContext = zip(Speaker, Institution, TalkTitle)
    return render(request,'./beta/4-2_workshopsSessionEpisode_beta.html',{'workshopsVideo':workshopsVideo['Video '+str(selectedSpeakerNumber)],
                                                                          'workshopsTalkTitle':workshopsTalkTitle['Talk Title ' + str(selectedSpeakerNumber)],
                                                                          'selectedSpeaker':selectedSpeaker,
                                                                          'selectedWorkshops':selectedWorkshops,
                                                                          'selectedGenre':selectedGenre,
                                                                          'WorkshopsContext':WorkshopsContext,
                                                                          'account':iros2020_emailinput})
#########################################################################################################
#########################################################################################################
#########################################################################################################
#Suggestions on each Pavilion Episodes
def suggestion(request):
    suggestedNum = request.GET['id1']
    findTitle = icra_example[(icra_example['Nr'] == int(suggestedNum))]
    titleName = findTitle['Title'].reset_index()
    VideoList = findTitle['VID'].reset_index()
    selectedTitle = titleName['Title'].iloc[0]
    suggestEpisodeNum = findSimilarTopic(int(suggestedNum))
    global iros2020_emailinput

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

    return render(request, './beta/4_pavilionSessionEpisode_beta.html', {'VideoList': VideoList['VID'],
                                                                         'Title': selectedTitle,
                                                                         'EpisodeContext': resultList,
                                                                         'account':iros2020_emailinput})


#########################################################################################################
#########################################################################################################
#########################################################################################################
#Search Results
def searchresult(request):
    inputKeyword = request.GET['id']
    # print(inputKeyword)
    resultNumber = searchByKeyword(inputKeyword)
    resultNumberlength = len(resultNumber)
    global iros2020_emailinput

    if not resultNumber:
        return render(request, './beta/6_searchResultError_beta.html', {'inputKeyword': inputKeyword})
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
        return render(request, './beta/5_searchResult_beta.html', {'EpisodeContext': resultList,
                                                                   'account':iros2020_emailinput})

#########################################################################################################
#########################################################################################################
#########################################################################################################
#My List
def mylist(request):
    global iros2020_emailinput
    return render(request,'./beta/7_myList_beta.html.html',{'account':iros2020_emailinput})