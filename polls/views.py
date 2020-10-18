# from django.shortcuts import render
#
# # Create your views here.
import json

from django.contrib import messages
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from polls.models import Papers, Comments, Users, Profile, VideoTimers
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from polls.tokens_beta import account_activation_token


from ipware import get_client_ip
import pandas as pd
import os
import math

from polls.forms_beta import SignUpForm

from polls.search import searchByKeyword, findSimilarTopic

pre = os.path.dirname(os.path.realpath(__file__))

# IROS2020 Excel file
excel_file0 = 'IROS20_OnDemand__10_05_main.xlsx'
path0 = os.path.join(pre, excel_file0)
iros2020_raw_orgin = pd.read_excel(path0, sheet_name=0)
iros2020_raw_orgin_empty_filter = iros2020_raw_orgin.fillna('missing')
iros2020_raw = iros2020_raw_orgin_empty_filter.iloc[0:1445,:] #Technical paper is from 0~1445
iros2020_award = iros2020_raw_orgin_empty_filter[(iros2020_raw_orgin_empty_filter['Theme']=='Award Finalists')] #IROS Award Session

#IROS2020 Session Chairs and Co-chairs
excel_file01 = 'IROS20_Sessions_Chairs.xlsx'
path01 = os.path.join(pre,excel_file01)
iros20_sessionChairs = pd.read_excel(path01,sheet_name=0)
iros20_sessionChairs = iros20_sessionChairs.fillna('missing')

# Call Keynotes and Plenaries
excel_file3 = 'IROS20_Specials.xlsx'
path3 = os.path.join(pre, excel_file3)
iros_specials = pd.read_excel(path3, sheet_name=0)
iros_specials = iros_specials.fillna('missing')

# Call Workshops and Tutorials
excel_file4 = 'IROS20_WSandTR.xlsx'
path4 = os.path.join(pre, excel_file4)
iros_wstr = pd.read_excel(path4, sheet_name=0)
iros_wstr = iros_wstr.fillna('missing')

# Call Partners
excel_file6 = 'IROS20_Partners.xlsx'
path6 = os.path.join(pre, excel_file6)
iros_partners = pd.read_excel(path6, sheet_name=0)
iros_partners = iros_partners.fillna('missing')

# Call Competition
excel_file7 = 'IROS20_Competition.xlsx'
path7 = os.path.join(pre,excel_file7)
iros_competition = pd.read_excel(path7,sheet_name=0)
iros_competition = iros_competition.fillna('missing')

iros_sessiontitle = iros2020_raw['Theme']
totalGenre = sorted(list(set(iros2020_raw['Theme'])))
# print(totalGenre)
organizedGenre = ['Award Finalists',
                  totalGenre[0],
                  totalGenre[2],
                  totalGenre[9],
                  totalGenre[6],
                  totalGenre[8],
                  totalGenre[3],
                  totalGenre[1],
                  totalGenre[10],
                  totalGenre[4],
                  totalGenre[5],
                  totalGenre[11],
                  totalGenre[7],
                  ]

Pavilion1 = iros2020_award[iros2020_award['Theme']==organizedGenre[0]] #Award Sessions
Pavilion2 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[1]]
Pavilion3 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[2]]
Pavilion4 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[3]]
Pavilion5 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[4]]
Pavilion6 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[5]]
Pavilion7 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[6]]
Pavilion8 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[7]]
Pavilion9 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[8]]
Pavilion10 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[9]]
Pavilion11 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[10]]
Pavilion12 = iros2020_raw[iros2020_raw['Theme']==organizedGenre[11]]
Pavilion13 = iros2020_raw[(iros2020_raw['Theme']==organizedGenre[12])]

Sessions1 = sorted(list(set(Pavilion1['Session title'])))
Sessions2 = sorted(list(set(Pavilion2['Session title'])))
Sessions3 = sorted(list(set(Pavilion3['Session title'])))
Sessions4 = sorted(list(set(Pavilion4['Session title'])))
Sessions5 = sorted(list(set(Pavilion5['Session title'])))
Sessions6 = sorted(list(set(Pavilion6['Session title'])))
Sessions7 = sorted(list(set(Pavilion7['Session title'])))
Sessions8 = sorted(list(set(Pavilion8['Session title'])))
Sessions9 = sorted(list(set(Pavilion9['Session title'])))
Sessions10 = sorted(list(set(Pavilion10['Session title'])))
Sessions11 = sorted(list(set(Pavilion11['Session title'])))
Sessions12 = sorted(list(set(Pavilion12['Session title'])))
Sessions13 = sorted(list(set(Pavilion13['Session title'])))

# totalSessions = zip(Sessions1, Sessions2, Sessions3, Sessions4, Sessions5)
#
# pavilionDict1, pavilionDict2, pavilionDict3, pavilionDict4, pavilionDict5 = dict()
# for a,b,c,d,e in totalSessions:
#     pavilionDict1[a] = Cartegories['Pavilion'][0]
#     pavilionDict2[b] = Cartegories['Pavilion'][1]
#     pavilionDict3[c] = Cartegories['Pavilion'][2]
#     pavilionDict4[d] = Cartegories['Pavilion'][3]
#     pavilionDict5[e] = Cartegories['Pavilion'][4]
# SpecialsSession = sorted(list(set(Specials['Genre'])))

SpecialsSession = ['Plenaries', 'Keynotes', 'IROS Original Series', 'Award Winners', 'BiR-IROS: Black in Robotics IROS 2020']

# Workshops
Workshops = iros_wstr[(iros_wstr['Type'] == 'Workshop Paper')]
Tutorials = iros_wstr[(iros_wstr['Type'] == 'Tutorial Paper')]

WorkshopsSunday = Workshops[(Workshops['Date'].str[0]=='S') & (Workshops['Date'].str[1]=='u')]
WorkshopsThursday = Workshops[(Workshops['Date'].str[0]=='T') & (Workshops['Date'].str[1]=='h')]

TutorialsSunday = Tutorials[(Tutorials['Date'].str[0]=='S') & (Tutorials['Date'].str[1]=='u')]
TutorialsThursday = Tutorials[(Tutorials['Date'].str[0]=='T') & (Tutorials['Date'].str[1]=='h')]

WSSundaySession = sorted(list(set(WorkshopsSunday['Workshop Title'])))
WSThursdaySession = sorted(list(set(WorkshopsThursday['Workshop Title'])))

TRSundaySession = sorted(list(set(TutorialsSunday['Workshop Title'])))
TRThursdaySession = sorted(list(set(TutorialsThursday['Workshop Title'])))

PavilionWSTR = ['Workshops', 'More Workshops','Tutorials', 'More Tutorials']

#########################################################################################################
#########################################################################################################
#########################################################################################################
# Login !
@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('entrance_main')
    # print("not_authenticated")
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        # print(login_form)
        if login_form.is_valid():
            login_account = login_form.cleaned_data.get('username')
            login_user = User.objects.filter(username__iexact=login_account)
            login_user_id = login_user[0].id
            ip, is_routable = get_client_ip(request)
            Profile.objects.filter(user_id=login_user_id).update(ip=ip)

            if login_user[0].is_superuser is True:
                auth_login(request, login_form.get_user())
                return redirect('entrance_main')
            else:
                messages.info(request, 'Please visit again IROS On-Demand when it opens on October 25th, 2020.')
                return redirect('login_main')

        else:
            # print("not_valid")
            messages.info(request, 'Please enter a correct username.')
            return redirect('login_main')

    return render(request, './1_login.html')


# Logout
def logout(request):
    auth_logout(request)
    return redirect('login_main')


# Login Authentication
@login_required()
def user_verification(request):
    return request.user.is_authenticated


#########################################################################################################
#########################################################################################################
#########################################################################################################
@csrf_exempt
def entrance(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)

    return render(request, './2_1entrance.html')


@csrf_exempt
def main(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)

    UserName = request.user.first_name + ' ' + request.user.last_name

    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    global clickToggleName

    if request.method == 'GET' and 'id' in request.GET:
        clickToggleName = request.GET['id']
    # print(request.GET)

    if clickToggleName == 'technicalpaper':
        showcontents = 1
    elif clickToggleName == 'wstr':
        showcontents = 2
    else:
        showcontents = 3

    allowWSContents = 1
    # if current_account.accesswstr.accessibility == True:
    #     allowWSContents = 1
    # else:
    #     allowWSContents = 0

    ##Technical talk and specials
    partnerName = []
    partnerLevel = []
    specialKeynoteSpeaker = []
    specialKNTitle = []
    specialKNNumber = []
    for i in organizedGenre:
        partner1 = iros_partners[(iros_partners['Theme'] == i)]
        keynotes = iros_specials[(iros_specials['Location'] == i)].reset_index()
        if partner1.empty is True:
            partnerName2 = 'missing'
            partnerLevel2 = 'missing'
        else:
            partnerName1 = partner1['Name'].reset_index()
            partnerName2 = partnerName1['Name'].iloc[0]
            partnerLevel1 = partner1['Cartegory'].reset_index()
            partnerLevel2 = partnerLevel1['Cartegory'].iloc[0]

        if keynotes.empty is True:
            KNspeaker = 'missing'
            KNTitle = 'missing'
            KNNumber = 'missing'
        else:
            KNspeaker = keynotes['Speaker'].iloc[0]
            KNTitle = keynotes['Title'].iloc[0]
            KNNumber = keynotes['Nr'].iloc[0]

        partnerName.append(partnerName2)
        partnerLevel.append(partnerLevel2)
        specialKeynoteSpeaker.append(KNspeaker)
        specialKNTitle.append(KNTitle)
        specialKNNumber.append(KNNumber)

    SpecialPavilion = 'IROS Specials'

    Sessions = [Sessions1, Sessions2, Sessions3, Sessions4, Sessions5, Sessions6, Sessions7,
                Sessions8, Sessions9, Sessions10, Sessions11, Sessions12, Sessions13]

    PavSessions = zip(organizedGenre, Sessions, partnerName, partnerLevel, specialKeynoteSpeaker, specialKNTitle,
                      specialKNNumber)

    ##WS/TR

    WSSundayNumber = []
    WSThursdayNumber = []
    TRSundaySNumber = []
    TRThursdayNumber = []

    for i in range(len(WSSundaySession)):
        Workshopslist = WorkshopsSunday[(WorkshopsSunday['Workshop Title'] == WSSundaySession[i])].reset_index()
        WSSundayNumber.append(Workshopslist['WS/TR Nr'].iloc[0])
    for j in range(len(WSThursdaySession)):
        Workshopslist = WorkshopsThursday[(WorkshopsThursday['Workshop Title'] == WSThursdaySession[j])].reset_index()
        WSThursdayNumber.append(Workshopslist['WS/TR Nr'].iloc[0])
    for k in range(len(TRSundaySession)):
        Workshopslist = TutorialsSunday[(TutorialsSunday['Workshop Title'] == TRSundaySession[k])].reset_index()
        TRSundaySNumber.append(Workshopslist['WS/TR Nr'].iloc[0])
    for l in range(len(TRThursdaySession)):
        Workshopslist = TutorialsThursday[(TutorialsThursday['Workshop Title'] == TRThursdaySession[l])].reset_index()
        TRThursdayNumber.append(Workshopslist['WS/TR Nr'].iloc[0])

    SessionWSTRName = [WSSundaySession, WSThursdaySession, TRSundaySession, TRThursdaySession]
    SessionWSTRNumber = [WSSundayNumber, WSThursdayNumber, TRSundaySNumber, TRThursdayNumber]
    PavWSTR = zip(PavilionWSTR, SessionWSTRName, SessionWSTRNumber)

    # Competition
    competitionNumber = iros_competition['Nr'].reset_index()
    competitionTitle = iros_competition['Title'].reset_index()
    PavCompetition = zip(competitionNumber['Nr'], competitionTitle['Title'])

    return render(request, './2_2main.html',
                  {'PavSessions':PavSessions,
                   'SpecialPavilion': SpecialPavilion,
                   'Specials': SpecialsSession,
                   'PavWSTR': PavWSTR,
                   'UserName': UserName,
                   'allowWSContents': allowWSContents,
                   'showcontents': showcontents,
                   'PavCompetition':PavCompetition,
                   })


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Sessions : Pavilion, Specials, Workshops
@login_required
def tvshow(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    # print(1)
    current_account = get_object_or_404(User, username=current_user)

    selectedSession = request.GET['id']
    selectedPavilion = request.GET['id2']
    selectedPavilionNum = request.GET['id3']

    if selectedPavilion == organizedGenre[0]:
        selectedSessionList = Sessions1
    elif selectedPavilion == organizedGenre[1]:
        selectedSessionList = Sessions2
    elif selectedPavilion == organizedGenre[2]:
        selectedSessionList = Sessions3
    elif selectedPavilion == organizedGenre[3]:
        selectedSessionList = Sessions4
    elif selectedPavilion == organizedGenre[4]:
        selectedSessionList = Sessions5
    elif selectedPavilion == organizedGenre[5]:
        selectedSessionList = Sessions6
    elif selectedPavilion == organizedGenre[6]:
        selectedSessionList = Sessions7
    elif selectedPavilion == organizedGenre[7]:
        selectedSessionList = Sessions8
    elif selectedPavilion == organizedGenre[8]:
        selectedSessionList = Sessions9
    elif selectedPavilion == organizedGenre[9]:
        selectedSessionList = Sessions10
    elif selectedPavilion == organizedGenre[10]:
        selectedSessionList = Sessions11
    elif selectedPavilion == organizedGenre[11]:
        selectedSessionList = Sessions12
    elif selectedPavilion == organizedGenre[12]:
        selectedSessionList = Sessions13
    else:
        selectedSessionList = []

    if selectedPavilion == organizedGenre[0]:
        AwardList = iros2020_award[(iros2020_award['Session title'] == selectedSession)]
        AwardTitleList = AwardList['Title'].reset_index()
        findPaperinRaw = iros2020_raw[(iros2020_raw['Title']) == AwardTitleList['Title'].iloc[0]]

        for awardListNum in range(1, len(AwardTitleList)):
            sorting = findPaperinRaw.append(
                iros2020_raw[(iros2020_raw['Title']) == AwardTitleList['Title'].iloc[awardListNum]])
            findPaperinRaw = sorting
        EpisodeList = findPaperinRaw
        TitleList = EpisodeList['Title'].reset_index()
        PDFList = EpisodeList['FN'].reset_index()
        titleNumber = EpisodeList['Nr'].reset_index()
    else:
        EpisodeList = iros2020_raw[(iros2020_raw['Session title'] == selectedSession)]
        TitleList = EpisodeList['Title'].reset_index()
        PDFList = EpisodeList['FN'].reset_index()
        titleNumber = EpisodeList['Nr'].reset_index()

    awardeeCount = []
    awardNameCount = []
    for titles in TitleList['Title']:
        titleMatch = iros2020_award[(iros2020_award['Title'] == titles)]
        if titleMatch.empty is True:
            awardConut = 0
            awardName = ''
        else:
            awardConut = 1
            awardName1 = titleMatch['Session title'].reset_index()
            awardName = awardName1['Session title'].iloc[0]
        awardNameCount.append(awardName)
        awardeeCount.append(awardConut)

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
    Video = EpisodeList['VID'].reset_index()

    # Partner information
    partnerSession = iros_partners[(iros_partners['Location'] == selectedSession)].reset_index()
    partnerName = partnerSession['Name'].reset_index()
    # print(selectedSession)
    partnerVideo = partnerSession['Video Name'].reset_index()
    partenerWebpage = partnerSession['Webpage Link'].reset_index()
    partnerVideoType = partnerSession['Type'].reset_index()
    partnerVideoLink = partnerSession['Video Link'].reset_index()
    partnerCartegory = partnerSession['Cartegory'].reset_index()
    partnerAbstract = partnerSession['Abstract'].reset_index()

    # Session Chair and Co-Chairs
    findSession = iros20_sessionChairs[(iros20_sessionChairs['Session title'] == selectedSession)].reset_index()
    findChair = findSession[(findSession['Role'] == 'Chair')].reset_index()
    findCoChair = findSession[(findSession['Role'] == 'Co-chair')].reset_index()
    ChairName = findChair['FirstName'].iloc[0] + findChair['LastName'].iloc[0]
    ChairAffiliation = findChair['Affiliation'].iloc[0]
    coChairName = findCoChair['FirstName'].iloc[0] + findCoChair['LastName'].iloc[0]
    coChairAffiliation = findCoChair['Affiliation'].iloc[0]
    Overview = findChair['Overview'].iloc[0]

    if request.method == "GET":
        paperLikeCount = []
        paperLikeButtonColor = []
        paperSaveButtonStatus = []
        paperHitCount = []
        for titleNr in titleNumber['Nr']:
            paper = get_object_or_404(Papers, paper_id=titleNr)
            # print(2)
            if current_account in paper.like_users.all():
                buttonColor = 1
            else:
                buttonColor = 0

            paperLikeButtonColor.append(buttonColor)
            paperLikeCount.append(paper.like_users.count())

            if current_account in paper.save_users.all():
                buttonStatus = 1
            else:
                buttonStatus = 0

            paperSaveButtonStatus.append(buttonStatus)

            paperHitCount.append(paper.paper_hitcount)

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
                             PDFList['FN'], titleNumber['Nr'], paperLikeCount, paperLikeButtonColor,
                             paperSaveButtonStatus, paperHitCount, awardeeCount, awardNameCount, Video['VID'])
        return render(request, './3_pavilionSession.html', {'Pavilion': selectedPavilion,
                                                            'PavilionNum': selectedPavilionNum,
                                                            'SessionList': selectedSessionList,
                                                            'Session': selectedSession,
                                                            'EpisodeContext': EpisodeContext,
                                                            'partnerCartegory':partnerCartegory['Cartegory'],
                                                            'partnerName': partnerName['Name'],
                                                            'partnerVideo': partnerVideo['Video Name'],
                                                            'partnerSession': partnerSession[
                                                                'Location'],
                                                            'partenerWebpage': partenerWebpage['Webpage Link'],
                                                            'partnerVideoType':partnerVideoType['Type'],
                                                            'partnerVideoLink':partnerVideoLink['Video Link'],
                                                            'partnerAbstract':partnerAbstract['Abstract'],
                                                            'Overview':Overview,
                                                            'ChairName':ChairName,
                                                            'coChairName':coChairName,
                                                            'ChairAffiliation':ChairAffiliation,
                                                            'coChairAffiliation':coChairAffiliation
                                                            })


def specials(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    selectedSpecial = request.GET['id']
    specialEpisodeList = iros_specials[(iros_specials['Genre'] == selectedSpecial)]
    speakerName = specialEpisodeList['Speaker'].reset_index()
    speakerBiography = specialEpisodeList['Bio'].reset_index()
    specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
    specialEpisodeNumber = specialEpisodeList['Nr'].reset_index()
    specialEpisodeTitle = specialEpisodeList['Title'].reset_index()
    speakerAffiliation = specialEpisodeList['Affiliation'].reset_index()
    speakerVideo = specialEpisodeList['Video'].reset_index()

    specialLikeCount = []
    specialLikeButtonColor = []
    specialSaveButtonStatus = []
    specialHitCount = []

    for specialNr in specialEpisodeNumber['Nr']:
        paper = get_object_or_404(Papers, paper_id=specialNr)
        if current_account in paper.like_users.all():
            buttonColor = 1
        else:
            buttonColor = 0
        specialLikeButtonColor.append(buttonColor)
        specialLikeCount.append(paper.like_users.count())

        if current_account in paper.save_users.all():
            buttonStatus = 1
        else:
            buttonStatus = 0
        specialSaveButtonStatus.append(buttonStatus)

        specialHitCount.append(paper.paper_hitcount)

    specialEpisodeContext = zip(speakerName['Speaker'],
                                speakerBiography['Bio'],
                                specialEpisodeAbstract['Abstract'],
                                specialEpisodeNumber['Nr'], specialLikeCount, specialLikeButtonColor,
                                specialSaveButtonStatus, specialHitCount, specialEpisodeTitle['Title'],
                                speakerAffiliation['Affiliation'],speakerVideo['Video']
                                )

    return render(request, './3-1_plenariesSession.html', {'selectedSpecial': selectedSpecial,
                                                           'specialEpisodeContext': specialEpisodeContext,
                                                           'SpecialsSession': SpecialsSession,
                                                           })


def workshops(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    selectedWorkshopsNumber = request.GET['id']
    selectedGenre = request.GET['id2']

    if selectedGenre == PavilionWSTR[0]:
        WorkshopsSession = WSSundaySession
        WorkshopDate = WorkshopsSunday
    elif selectedGenre == PavilionWSTR[1]:
        WorkshopsSession = WSThursdaySession
        WorkshopDate = WorkshopsThursday
    elif selectedGenre == PavilionWSTR[2]:
        WorkshopsSession = TRSundaySession
        WorkshopDate = TutorialsSunday
    elif selectedGenre == PavilionWSTR[3]:
        WorkshopsSession = TRThursdaySession
        WorkshopDate = TutorialsThursday
    else:
        WorkshopsSession = []

    workshopSessionNumbers = []
    for i in range(len(WorkshopsSession)):
        Workshopslist = WorkshopDate[(WorkshopDate['Workshop Title'] == WorkshopsSession[i])].reset_index()
        workshopSessionNumbers.append(Workshopslist['WS/TR Nr'].iloc[0])

    workshopsEpisodeList = iros_wstr[(iros_wstr['WS/TR Nr'] == selectedWorkshopsNumber)].reset_index()
    WorkshopsTitle = workshopsEpisodeList['Workshop Title'].iloc[0]
    workshopsHomepage = workshopsEpisodeList['Webpage'].iloc[0]
    workshopAbstract = workshopsEpisodeList['Workshop Abstract'].iloc[0]
    workshopOrganizers = []
    workshopOrganizersAfilliation = []
    for i in range(1, 11):
        workshopOrganizers.append(workshopsEpisodeList['Organizer' + str(i)].iloc[0])
        workshopOrganizersAfilliation.append(workshopsEpisodeList['Organizer' + str(i) + 'Affil'].iloc[0])

    workshopOrganizersInfo = zip(workshopOrganizers, workshopOrganizersAfilliation)

    workshopNumber = workshopsEpisodeList['Nr'].reset_index()
    Speaker = workshopsEpisodeList['Speaker'].reset_index()
    Institution = workshopsEpisodeList['Institution'].reset_index()
    Talktitle = workshopsEpisodeList['Title'].reset_index()
    Video = workshopsEpisodeList['Video'].reset_index()
    Abstract = workshopsEpisodeList['Presentation Abstract'].reset_index()
    Dummy = workshopsEpisodeList['Dummy'].reset_index()

    workshopLikeCount = []
    workshopLikeButtonColor = []
    workshopSaveButtonStatus = []
    workshopHitCount = []
    for workshopNr in workshopNumber['Nr']:
        paper = get_object_or_404(Papers, paper_id=int(workshopNr))
        if current_account in paper.like_users.all():
            buttonColor = 1
        else:
            buttonColor = 0
        workshopLikeButtonColor.append(buttonColor)
        workshopLikeCount.append(paper.like_users.count())

        if current_account in paper.save_users.all():
            buttonStatus = 1
        else:
            buttonStatus = 0
        workshopSaveButtonStatus.append(buttonStatus)
        workshopHitCount.append(paper.paper_hitcount)

    # print(workshopLikeButtonColor)
    WorkshopsContext = zip(Speaker['Speaker'], Institution['Institution'], Talktitle['Title'], workshopNumber['Nr'],
                           workshopLikeButtonColor,
                           workshopLikeCount, workshopSaveButtonStatus, workshopHitCount, Video['Video'],
                           Abstract['Presentation Abstract'], Dummy['Dummy'])

    count = 0
    for k in range(len(Video['Video'])):
        if Video['Video'].iloc[k] == 'missing':
            count += 1
        if count == len(Video['Video']):
            noShowContents = 1
        else:
            noShowContents = 0

    return render(request, './3-2_workshopsSession.html', {'selectedWorkshopsNumber': selectedWorkshopsNumber,
                                                           'selectedWorkshopsTitle':WorkshopsTitle,
                                                           'workshopAbstract':workshopAbstract,
                                                           'selectedGenre': selectedGenre,
                                                           'WorkshopsContext': WorkshopsContext,
                                                           'WorkshopsSession': WorkshopsSession,
                                                           'workshopSessionNumbers':workshopSessionNumbers,
                                                           'workshopsHomepage': workshopsHomepage,
                                                           'workshopOrganizersInfo':workshopOrganizersInfo,
                                                           'noShowContents':noShowContents
                                                           })

def competition(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    selectedCompetitionNumber= request.GET['id']

    findCompetition=iros_competition[(iros_competition['Nr']==int(selectedCompetitionNumber))].reset_index()

    CompetitionTitle = findCompetition['Title'].iloc[0]
    CompetitionHomepage = findCompetition['Webpage'].iloc[0]
    CompetitionLive = findCompetition['LiveStream'].iloc[0]
    CompetitionDate = findCompetition['Date'].iloc[0]
    CompetitionDescription = findCompetition['Description'].iloc[0]
    CompetitionVideo = findCompetition['Video'].iloc[0]
    CompetitionOrganizers = []
    CompetitionOrganizersAfilliation = []
    for i in range(1, 8):
        CompetitionOrganizers.append(findCompetition['Organizer' + str(i)].iloc[0])
        CompetitionOrganizersAfilliation.append(findCompetition['Affiliation' + str(i)].iloc[0])

    CompetitionOrganizersInfo = zip(CompetitionOrganizers, CompetitionOrganizersAfilliation)

    # Competition
    competitionNumber = iros_competition['Nr'].reset_index()
    competitionTitle = iros_competition['Title'].reset_index()
    PavCompetition = zip(competitionNumber['Nr'], competitionTitle['Title'])

    return render(request,'./beta/3-3_competitionSession_beta.html',{'selectedCompetitionNumber':selectedCompetitionNumber,
                                                                     'CompetitionTitle':CompetitionTitle,
                                                                     'CompetitionHomepage':CompetitionHomepage,
                                                                     'CompetitionLive':CompetitionLive,
                                                                     'CompetitionDate':CompetitionDate,
                                                                     'CompetitionDescription':CompetitionDescription,
                                                                     'CompetitionVideo':CompetitionVideo,
                                                                     'CompetitionOrganizersInfo':CompetitionOrganizersInfo,
                                                                     'PavCompetition':PavCompetition,
                                                                     })
#########################################################################################################
#########################################################################################################
#########################################################################################################
# Episodes : Pavilion, Specials, Workshops
def episode(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    selectedNumber = request.GET['id']
    selectedSession = request.GET['id2']

    findVideo = iros2020_raw[(iros2020_raw['Nr'] == int(selectedNumber))]
    VideoList = findVideo['VID'].reset_index()
    selectedTitle = findVideo['Title'].reset_index()
    suggestEpisodeNum = findSimilarTopic(int(selectedNumber))
    # print(selectedTitle)
    similarPaper = iros2020_raw[(iros2020_raw['Nr'] == int(suggestEpisodeNum[0]))]

    for i in range(1, 12):
        main2 = similarPaper.append(iros2020_raw[(iros2020_raw['Nr'] == int(suggestEpisodeNum[i]))])
        similarPaper = main2
    # print(similarPaper)
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
    SessionTitle = similarPaper['Session title'].reset_index()
    Video = similarPaper['VID'].reset_index()

    TitleList = similarPaper['Title'].reset_index()
    PDFList = similarPaper['FN'].reset_index()
    titleNumber = similarPaper['Nr'].reset_index()

    awardeeCount = []
    awardNameCount = []
    for titles in TitleList['Title']:
        titleMatch = iros2020_award[(iros2020_award['Title'] == titles)]
        if titleMatch.empty is True:
            awardConut = 0
            awardName = ''
        else:
            awardConut = 1
            awardName1 = titleMatch['Session title'].reset_index()
            awardName = awardName1['Session title'].iloc[0]
        awardNameCount.append(awardName)
        awardeeCount.append(awardConut)

    # Comments load area
    lengthComments = Comments.objects.filter(paper_id=int(selectedNumber)).count()
    arrayComments = []
    for ac in range(lengthComments):
        arrayComments.append(Comments.objects.filter(paper_id=int(selectedNumber))[ac].comment)

    paperLikeCount = []
    paperLikeButtonColor = []
    paperSaveButtonStatus = []
    paperHitCount = []

    if request.method == "GET":
        selectedPaper = get_object_or_404(Papers, paper_id=int(selectedNumber))

        if current_account in selectedPaper.like_users.all():
            selectedPaperLikeButtonColor = 1
        else:
            selectedPaperLikeButtonColor = 0
        selectedPaperLikeCount = selectedPaper.like_users.count()

        if current_account in selectedPaper.save_users.all():
            selectedPaperbuttonStatus = 1
        else:
            selectedPaperbuttonStatus = 0

        selectedpaperHitCount = int(selectedPaper.paper_hitcount) + 1

        for titleNr in titleNumber['Nr']:
            paper = get_object_or_404(Papers, paper_id=titleNr)
            if current_account in paper.like_users.all():
                buttonColor = 1
            else:
                buttonColor = 0
            paperLikeButtonColor.append(buttonColor)
            paperLikeCount.append(paper.like_users.count())

            if current_account in paper.save_users.all():
                buttonStatus = 1
            else:
                buttonStatus = 0
            paperSaveButtonStatus.append(buttonStatus)

            paperHitCount.append(paper.paper_hitcount)

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
                         PDFList['FN'], titleNumber['Nr'], paperLikeCount, paperLikeButtonColor,
                         SessionTitle['Session title'], paperSaveButtonStatus, paperHitCount, awardeeCount,
                         awardNameCount, Video['VID'])
        return render(request, './4_pavilionSessionEpisode.html', {'VideoList': VideoList['VID'],
                                                                   'Title': selectedTitle['Title'],
                                                                   'Session': selectedSession,
                                                                   'EpisodeContext': resultList,
                                                                   'SelectedPaperNumber':
                                                                       selectedNumber,
                                                                   'selectedpaperHitCount':selectedpaperHitCount,
                                                                   'selectedPaperLikeButtonColor': selectedPaperLikeButtonColor,
                                                                   'selectedPaperLikeCount': selectedPaperLikeCount,
                                                                   'selectedPaperbuttonStatus': selectedPaperbuttonStatus,
                                                                   'arrayComments': arrayComments,
                                                                   'lengthComments': lengthComments
                                                                   })


def specialsepisode(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    # Selected Specials
    selectedSpecialNr = request.GET['id']
    selectedSpecial = request.GET['id2']
    findspeaker = iros_specials[(iros_specials['Nr'] == int(selectedSpecialNr))].reset_index()
    selectedSpeaker = findspeaker['Speaker'].iloc[0]
    selectedTitle = findspeaker['Title'].iloc[0]
    specialVideo = findspeaker['Video'].iloc[0]

    # Other Specials
    specialEpisodeList = iros_specials[(iros_specials['Genre'] == selectedSpecial)]
    speakerName = specialEpisodeList['Speaker'].reset_index()
    speakerBiography = specialEpisodeList['Bio'].reset_index()
    specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
    specialEpisodeNumber = specialEpisodeList['Nr'].reset_index()
    specialEpisodeTitle = specialEpisodeList['Title'].reset_index()
    specialEpisodeAffiliation = specialEpisodeList['Affiliation'].reset_index()

    # Comments load area
    lengthComments = Comments.objects.filter(paper_id=int(selectedSpecialNr)).count()
    arrayComments = []
    for ac in range(lengthComments):
        arrayComments.append(Comments.objects.filter(paper_id=int(selectedSpecialNr))[ac].comment)

    if request.method == "GET":
        selectedSpecialLike = get_object_or_404(Papers, paper_id=int(selectedSpecialNr))

        selectedSpecialHitCount = int(selectedSpecialLike.paper_hitcount) + 1
        # Selected Sepcial Like
        if current_account in selectedSpecialLike.like_users.all():
            selectedSpecialLikeButtonColor = 1
        else:
            selectedSpecialLikeButtonColor = 0
        selectedSpecialLikeCount = selectedSpecialLike.like_users.count()

        if current_account in selectedSpecialLike.save_users.all():
            selectedSpecialSaveButtonStatus = 1
        else:
            selectedSpecialSaveButtonStatus = 0

        # Other Sepcial Like
        specialLikeCount = []
        specialLikeButtonColor = []
        specialSaveButtonStatus = []
        specialHitCount = []

        for specialNr in specialEpisodeNumber['Nr']:
            paper = get_object_or_404(Papers, paper_id=specialNr)
            if current_account in paper.like_users.all():
                buttonColor = 1
            else:
                buttonColor = 0
            specialLikeButtonColor.append(buttonColor)
            specialLikeCount.append(paper.like_users.count())

            if current_account in paper.save_users.all():
                buttonStatus = 1
            else:
                buttonStatus = 0
            specialSaveButtonStatus.append(buttonStatus)

            specialHitCount.append(paper.paper_hitcount)

        specialEpisodeContext = zip(speakerName['Speaker'],
                                    speakerBiography['Bio'],
                                    specialEpisodeAbstract['Abstract'],
                                    specialEpisodeNumber['Nr'], specialLikeCount, specialLikeButtonColor,
                                    specialSaveButtonStatus, specialHitCount, specialEpisodeTitle['Title'],
                                    specialEpisodeAffiliation['Affiliation']
                                    )

    return render(request, './4-1_plenariesSessionEpisode.html', {'specialVideo': specialVideo,
                                                                  'selectedSpecial': selectedSpecial,
                                                                  'selectedTitle':selectedTitle,
                                                                  'specialEpisodeContext': specialEpisodeContext,
                                                                  'selectedSpecialLikeCount': selectedSpecialLikeCount,
                                                                  'selectedSpecialLikeButtonColor': selectedSpecialLikeButtonColor,
                                                                  'selectedSpecialSaveButtonStatus': selectedSpecialSaveButtonStatus,
                                                                  'SelectedPaperNumber':
                                                                      selectedSpecialNr,
                                                                  'arrayComments': arrayComments,
                                                                  'lengthComments': lengthComments,
                                                                  'selectedSpecialHitCount':selectedSpecialHitCount,
                                                                  })


def workshopsepisode(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    selectedTitleNumber = request.GET['id']
    selectedWorkshopsNumber = request.GET['id2']

    findWorkshop = iros_wstr[(iros_wstr['Nr'] == int(selectedTitleNumber))].reset_index()
    selectedWorkshopTalkTitle = findWorkshop['Title'].iloc[0]
    selectedWorkshopVideo = findWorkshop['Video'].iloc[0]
    selectedWorkshopTitle = findWorkshop['Workshop Title'].iloc[0]
    findWSorTR = findWorkshop['WS/TR Nr'].iloc[0]

    if findWSorTR[0] == 'W':
        WSorTR = 1
    else:
        WSorTR = 0

    # Comments load area
    lengthComments = Comments.objects.filter(paper_id=int(selectedTitleNumber)).count()
    arrayComments = []
    for ac in range(lengthComments):
        arrayComments.append(Comments.objects.filter(paper_id=int(selectedTitleNumber))[ac].comment)

    if request.method == "GET":
        # Selected Workshop Like, MyList
        selectedWorkshopLike = get_object_or_404(Papers, paper_id=int(selectedTitleNumber))

        selectedWorkshopHitCount = int(selectedWorkshopLike.paper_hitcount) + 1

        if current_account in selectedWorkshopLike.like_users.all():
            selectedWorkshopLikeButtonColor = 1
        else:
            selectedWorkshopLikeButtonColor = 0
        selectedWorkshopLikeCount = selectedWorkshopLike.like_users.count()

        if current_account in selectedWorkshopLike.save_users.all():
            selectedWorkshopSaveButtonStatus = 1
        else:
            selectedWorkshopSaveButtonStatus = 0

        workshopsEpisodeList = iros_wstr[(iros_wstr['WS/TR Nr'] == selectedWorkshopsNumber)].reset_index()
        workshopsVideo = workshopsEpisodeList['Video'].reset_index()
        workshopNumber = workshopsEpisodeList['Nr'].reset_index()
        workshopSpeaker = workshopsEpisodeList['Speaker'].reset_index()
        workshopInstitution = workshopsEpisodeList['Institution'].reset_index()
        workshopTitle = workshopsEpisodeList['Title'].reset_index()
        workshopAbstract = workshopsEpisodeList['Presentation Abstract'].reset_index()
        workshopDummy = workshopsEpisodeList['Dummy'].reset_index()

        # Other Workshops Like
        workshopLikeCount = []
        workshopLikeButtonColor = []
        workshopSaveButtonStatus = []
        workshopHitCount = []

        for workshopNr in workshopNumber['Nr']:
            paper = get_object_or_404(Papers, paper_id=int(workshopNr))
            if current_account in paper.like_users.all():
                buttonColor = 1
            else:
                buttonColor = 0
            workshopLikeButtonColor.append(buttonColor)
            workshopLikeCount.append(paper.like_users.count())

            if current_account in paper.save_users.all():
                buttonStatus = 1
            else:
                buttonStatus = 0
            workshopSaveButtonStatus.append(buttonStatus)

            workshopHitCount.append(paper.paper_hitcount)

        WorkshopsContext = zip(workshopSpeaker['Speaker'], workshopInstitution['Institution'], workshopTitle['Title'],
                               workshopNumber['Nr'], workshopLikeButtonColor,
                               workshopLikeCount, workshopSaveButtonStatus, workshopHitCount, workshopsVideo['Video'],
                               workshopAbstract['Presentation Abstract'], workshopDummy['Dummy'])

        return render(request, './4-2_workshopsSessionEpisode.html',
                      {'workshopsVideo': selectedWorkshopVideo,
                       'workshopsTalkTitle': selectedWorkshopTalkTitle,
                       'selectedWorkshops': selectedWorkshopTitle,
                       'selectedWorkshopsNumber': selectedWorkshopsNumber,
                       'WorkshopsContext': WorkshopsContext,
                       'selectedWorkshopEpisodeNumber': selectedTitleNumber,
                       'selectedWorkshopLikeButtonColor': selectedWorkshopLikeButtonColor,
                       'selectedWorkshopLikeCount': selectedWorkshopLikeCount,
                       'selectedWorkshopSaveButtonStatus': selectedWorkshopSaveButtonStatus,
                       'arrayComments': arrayComments,
                       'lengthComments': lengthComments,
                       'selectedWorkshopHitCount': selectedWorkshopHitCount,
                       'WSorTR': WSorTR
                       })


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Search Results
def searchresult(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    inputKeyword = request.GET['id']
    showcontents = request.GET['id2']
    resultNumber = searchByKeyword(inputKeyword)

    # Filter workshop, tutorials, and finalists
    # filterOnlySession = []
    # for rawNumber in resultNumber:
    #     if rawNumber < 3140:
    #         filterOnlySession.append(rawNumber)
    # resultNumber = filterOnlySession
    resultNumberlength = len(resultNumber)

    if not resultNumber:
        return render(request, './beta/6_searchResultError_beta.html', {'inputKeyword': inputKeyword,
                                                                        'showcontents': int(showcontents)})
    else:
        searchTitle = iros2020_raw[(iros2020_raw['Nr'] == int(resultNumber[0]))]

        for i in range(1, resultNumberlength):
            main2 = searchTitle.append(iros2020_raw[(iros2020_raw['Nr'] == int(resultNumber[i]))])
            searchTitle = main2

        pavilionNumMatch = dict()
        for i in range(len(organizedGenre) - 1):
            pavilionNumMatch[organizedGenre[i + 1]] = i + 1

        # print(searchTitle)
        SessionList = searchTitle['Session title'].reset_index()
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
        pavilionList = searchTitle['Theme'].reset_index()
        VideoList = searchTitle['VID'].reset_index()

        pavilionNumList = []
        for i in pavilionList['Theme']:
            pavilionNumList.append(pavilionNumMatch[i])

        awardeeCount = []
        awardNameCount = []
        for titles in TitleList['Title']:
            titleMatch = iros2020_award[(iros2020_award['Title'] == titles)]
            if titleMatch.empty is True:
                awardConut = 0
                awardName = ''
            else:
                awardConut = 1
                awardName1 = titleMatch['Session title'].reset_index()
                awardName = awardName1['Session title'].iloc[0]
            awardNameCount.append(awardName)
            awardeeCount.append(awardConut)

        paperLikeCount = []
        paperLikeButtonColor = []
        paperSaveButtonStatus = []
        paperHitCount = []

        if request.method == "GET":

            for titleNr in titleNumber['Nr']:
                paper = get_object_or_404(Papers, paper_id=int(titleNr))

                if current_account in paper.like_users.all():
                    buttonColor = 1
                else:
                    buttonColor = 0

                paperLikeButtonColor.append(buttonColor)
                paperLikeCount.append(paper.like_users.count())

                if current_account in paper.save_users.all():
                    buttonStatus = 1
                else:
                    buttonStatus = 0

                paperSaveButtonStatus.append(buttonStatus)

                paperHitCount.append(paper.paper_hitcount)

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
                             PDFList['FN'], titleNumber['Nr'], paperLikeCount, paperLikeButtonColor,
                             paperSaveButtonStatus, SessionList['Session title'], paperHitCount, awardeeCount,
                             awardNameCount, pavilionList['Theme'], pavilionNumList, VideoList['VID'])

        return render(request, './5_searchResult.html', {'EpisodeContext': resultList,
                                                         'showcontents': int(showcontents)
                                                         })


#########################################################################################################
#########################################################################################################
#########################################################################################################

# My List
def mylist(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_account = request.user.username
    user = get_object_or_404(User, username=current_account)

    showcontents = request.GET['id']
    # print(showcontents)
    mylistQuery = user.save_papers.all()
    mylistNumber = mylistQuery.count()

    # Arrange Numbers by Genres
    mylistEpisodeNumber = []
    mylistSpecialNumber = []
    mylistWorkshopsNumber = []
    for i in range(mylistNumber):
        if mylistQuery[i].paper_id < 3140:
            mylistEpisodeNumber.append(mylistQuery[i].paper_id)
        elif mylistQuery[i].paper_id < 4000:
            mylistWorkshopsNumber.append(mylistQuery[i].paper_id)
        else:
            mylistSpecialNumber.append(mylistQuery[i].paper_id)

    # MyList Episodes
    if len(mylistEpisodeNumber) != 0:
        mylistEpisodeTitle = []
        mylistEpisodeSession = []
        for i in range(len(mylistEpisodeNumber)):
            mylistEpisode = iros2020_raw[(iros2020_raw['Nr'] == int(mylistEpisodeNumber[i]))].reset_index()
            mylistEpisodeSession.append(mylistEpisode['Session title'].iloc[0])
            mylistEpisodeTitle.append(mylistEpisode['Title'].iloc[0])

        mylistEpisodeContext = zip(mylistEpisodeTitle, mylistEpisodeSession, mylistEpisodeNumber)
    else:
        mylistEpisodeContext = []

    # MyList Specials
    if len(mylistSpecialNumber) != 0:

        mylistSpecialSpeaker = []
        mylistSpecialSpecial = []
        mylistSpecialTitle = []
        for j in range(len(mylistSpecialNumber)):
            mylistSpecial = iros_specials[(iros_specials['Nr'] == int(mylistSpecialNumber[j]))].reset_index()
            mylistSpecialSpeaker.append(mylistSpecial['Speaker'].iloc[0])
            mylistSpecialSpecial.append(mylistSpecial['Genre'].iloc[0])
            mylistSpecialTitle.append(mylistSpecial['Title'].iloc[0])

        mylistSpecialContext = zip(mylistSpecialSpeaker, mylistSpecialSpecial, mylistSpecialNumber, mylistSpecialTitle)
    else:
        mylistSpecialContext = []

    # MyList Workshops
    if len(mylistWorkshopsNumber) != 0:

        mylistWorkshopsNr = []
        mylistWorkshopsTalkNr = []
        mylistWorkshopsTitle = []
        for w in range(len(mylistWorkshopsNumber)):
            mylistWorkshops = iros_wstr[(iros_wstr['Nr'] == int(mylistWorkshopsNumber[w]))].reset_index()
            mylistWorkshopsNr.append(mylistWorkshops['WS/TR Nr'].iloc[0])
            mylistWorkshopsTalkNr.append(mylistWorkshops['Nr'].iloc[0])
            mylistWorkshopsTitle.append(mylistWorkshops['Title'].iloc[0])

        mylistWorkshopsContext = zip(mylistWorkshopsNr, mylistWorkshopsTalkNr, mylistWorkshopsTitle)
    else:
        mylistWorkshopsContext = []

    return render(request, './7_myList.html', {
        'mylistEpisodeNumber': len(mylistEpisodeNumber),
        'mylistEpisodeContext': mylistEpisodeContext,
        'mylistSpecialNumber': len(mylistSpecialNumber),
        'mylistSpecialContext': mylistSpecialContext,
        'mylistWorkshopsNumber': len(mylistWorkshopsNumber),
        'mylistWorkshopsContext': mylistWorkshopsContext,
        'showcontents': int(showcontents)
    })


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Like, Comment, MylistSave, hitcount Function
@csrf_exempt
def post_like(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    paperLikeCount = []

    if request.is_ajax:
        clickedPaperNumber = int(request.POST['paperNumber'])
        # print(clickedPaperNumber)
        paper = get_object_or_404(Papers, paper_id=clickedPaperNumber)

        if current_account in paper.like_users.all():
            paper.like_users.remove(current_account)
            buttonColor = "grey"
        else:
            paper.like_users.add(current_account)
            buttonColor = "yellow"
        # print(buttonColor)
        paperLikeCount.append(paper.like_users.count())
        response = {'likeButtonColor': buttonColor, 'likeCount': paperLikeCount}

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


@csrf_exempt
def add_comment(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    # print(current_account)
    # Comments load area
    if request.is_ajax:
        clickedPaperNumber = int(request.POST['paperNumber'])
        c1 = Comments(paper_id=clickedPaperNumber, comment=request.POST['comment'])
        c1.save()
        c1.comment_users.add(current_account)

        lengthComments = Comments.objects.filter(paper_id=clickedPaperNumber).count()

        response = {'commentAdded': str(lengthComments) + " : " + request.POST['comment'],
                    'lengthComments': lengthComments}

    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


@csrf_exempt
def post_save(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)
    current_user = request.user.username
    current_account = get_object_or_404(User, username=current_user)

    if request.is_ajax:
        clickedPaperNumber = int(request.POST['paperNumber'])
        paper = get_object_or_404(Papers, paper_id=clickedPaperNumber)
        # print(clickedPaperNumber)
        if current_account in paper.save_users.all():
            paper.save_users.remove(current_account)
            buttonStatus = 'fa fa-plus'
            buttonMessage = 'Add to my list'
        else:
            paper.save_users.add(current_account)
            buttonStatus = 'fa fa-check-circle'
            buttonMessage = 'Added to my list'
        # print(buttonMessage)

        response = {'paperSaveButtonStatus': buttonStatus, 'buttonMessage': buttonMessage}

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )


@csrf_exempt
def post_hitcount(request):
    if request.user.is_authenticated == False:
        return render(request, './1-1_loginError.html')
    else:
        user_verification(request)

    if request.is_ajax:
        clickedPaperNumber = int(request.POST['paperNumber'])
        paper = get_object_or_404(Papers, paper_id=clickedPaperNumber)

        # For Page edit
        # paperHitCount = 0

        # For active page
        paperHitCount = paper.paper_hitcount + 1

        Papers.objects.filter(paper_id=clickedPaperNumber).update(paper_hitcount=paperHitCount)
        response = {'hitCount': paperHitCount}

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

@csrf_exempt
def update_playtime(request):
    if request.user.is_authenticated == False:
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        user_verification(request)

    if request.is_ajax:
        video_number = int(request.POST['paperNumber'])
        video_playtime = int(request.POST['time'])
        vid_object = get_object_or_404(VideoTimers, paper_id=video_number)

        # For active page
        total_time = vid_object.seconds + video_playtime/1000

        VideoTimers.objects.filter(paper_id=video_number).update(seconds=total_time)
        response = {'total_time': total_time}

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
############################################################################
############################################################################
############################################################################

# dongbin1= []
# for users in ieeeusers.objects.raw('SELECT * FROM polls_like'):
#     dongbin = users.paperid
#     dongbin1.append(dongbin)
# print(dongbin1)
# ieeeusers.objects.filter(ieeeusers_id='iros1').update(ieeeusers_password='gyuhozzang')
# user1 = User.objects.create_user("torsten@kit.edu","torsten@kit.edu","a")
# user1.first_name = "Dr. Paul"
# user1.last_name = "Oh"
# user1.save()
#
# user2 = User.objects.create_user("leeg3@unlv.nevada.edu","leeg3@unlv.nevada.edu","a")
# user2.first_name = "Gyuho"
# user2.last_name = "Lee"
# user2.save()
# irosuser1 = User(iros2020_name="Dongbin Kim", iros2020_email="dongbin.kim@unlv.edu")
# irosuser2 = User(iros2020_name="Dr. Paul Oh", iros2020_email="paul.oh@unlv.edu")
# irosuser1.save()
# irosuser2.save()
# irosuser3 = User(iros2020_name="Gyuho Lee", iros2020_email="leeg3@unlv.nevada.edu")
# irosuser4 = User(iros2020_name="Blake Hament", iros2020_email="blakehament@gmail.com")
# irosuser3.save()
# irosuser4.save()

##Paper Database
# for i in range(1553):
#     db = Papers(paper_id=icra_example['Nr'][i])
#     db.save()
# # print(len(icra_specials['Nr']))
# for j in range(len(icra_specials['Nr'])):
#     db1 = Papers(paper_id=icra_specials['Nr'][j])
#     db1.save()
# #
# for k in range(len(icra_workshops['Workshop Number'])):
#     db2 = Papers(paper_id=icra_workshops['Workshop Number'][k])
#     db2.save()

# ip, is_routable = get_client_ip(request)
# print(ip)

# VideoTimers Initialization
# for i in range(1553):
#     db = VideoTimers(paper_id=icra_example['Nr'][i])
#     db.save()
# print(is_routable)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username__iexact=form.cleaned_data.get('email')).exists():
                existed_user = User.objects.filter(username__iexact=form.cleaned_data.get('email'))
                #IP store
                existed_user_id = existed_user[0].id
                ip, is_routable = get_client_ip(request)
                Profile.objects.filter(user_id=existed_user_id).update(ip=ip)

                if existed_user[0].is_active is True:
                    messages.info(request,
                                  'This email is already registered and activated, please try with different email address if this is a new registration')
                    return redirect('signup_main')
                else:
                    messages.warning(request,'This email is already registered, but not activated. Do you want the activation email to be sent again?')
                    messages.warning(request,'<button class="resendButton" type="submit" '
                                             'onclick="activationResend('+str(existed_user[0].pk)+')">Resend</button>')
                    return redirect('signup_main')

            user = form.save()
            user.refresh_from_db()

            ip, is_routable = get_client_ip(request)            # print(str(ip))

            user.profile.ip = ip
            user.profile.occupation = form.cleaned_data.get('occupation')
            user.profile.affiliation = form.cleaned_data.get('affiliation')
            user.profile.previous_attendance = form.cleaned_data.get('previous_attendance')
            user.profile.primary = form.cleaned_data.get('primary')
            user.profile.member = form.cleaned_data.get('member')
            user.profile.demographic_region = form.cleaned_data.get('demographic_region')

            user.is_active = False
            user.save()
            # user = authenticate(username=user.username, password='a')
            # auth_login(request, user)

            current_site = get_current_site(request)
            subject = 'Activate Your IROS2020 On-Demand Account'
            message = render_to_string('./0_4_account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,'ondemandinfo@iros2020.org')

            return redirect('account_activation_sent_main')
    else:
        form = SignUpForm()
    return render(request, './0_1_signup.html', {'form': form})

@csrf_exempt
def account_activation_sent(request):
    return render(request, './0_2_account_activation_sent.html')

@csrf_exempt
def resendactivation(request):
    if request.is_ajax:
        # print(request.POST['resendEmailAdress'])
        user_raw = User.objects.filter(pk=int(request.POST['resendEmailAdress']))
        user= user_raw[0]
        current_site = get_current_site(request)

        subject = 'Activate Your IROS2020 On-Demand Account'
        message = render_to_string('./0_4_account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message, 'ondemandinfo@iros2020.org')

        resentMessage = 'Verfication email is just re-sent, please check your inbox'
        response = {'resentMessage': resentMessage}
        # print('sent')
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        a = User.objects.filter(pk=uid)
        if len(a) == 0:
            return render(request, './beta/0_3_account_activate_invalid.html',status=500)

        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    user.refresh_from_db()
    user.profile.refresh_from_db()
    if user is not None and account_activation_token.check_token(user, token):
        if user.profile.email_confirmed is True:
            return render(request, './0_3_account_activate_invalid.html')
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()

        # print(1)
        # auth_login(request, user)

        # current_site = get_current_site(request)
        # subject = 'Congratulations! Your IROS2020 On-Demand Account Has Been Activated'
        # message = render_to_string('./0_5_account_activation_success.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        # })
        # user.email_user(subject, message,'ondemandinfo@iros2020.org')

        return render(request,'./0_5_account_activation_success.html',{'user':user})
    else:
        return render(request, './0_3_account_activate_invalid.html')
