# from django.shortcuts import render
#
# # Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from polls.models import Users, Papers, Comments
import pandas as pd
import os
import math

from polls.search import searchByKeyword, findSimilarTopic

# IROS2020 Registered List
iros2020registered_email = []
iros2020registered_name = []
mydict = dict()

for p in Users.objects.raw('SELECT * FROM polls_users'):
    iros2020registered_email.append(p.iros2020_email)
    iros2020registered_name.append(p.iros2020_name)
    mydict[p.iros2020_email] = p.iros2020_name

iros2020registered_db = Users.objects.all()
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
path4 = os.path.join(pre, excel_file4)
icra_workshops = pd.read_excel(path4, sheet_name=0)
icra_workshops = icra_workshops.fillna('missing')

# Call Sponsors
excel_file6 = 'ICRA20Sponsors.xlsx'
path6 = os.path.join(pre, excel_file6)
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

# totalSessions = zip(Sessions1, Sessions2, Sessions3, Sessions4, Sessions5)
#
# pavilionDict1, pavilionDict2, pavilionDict3, pavilionDict4, pavilionDict5 = dict()
# for a,b,c,d,e in totalSessions:
#     pavilionDict1[a] = Cartegories['Pavilion'][0]
#     pavilionDict2[b] = Cartegories['Pavilion'][1]
#     pavilionDict3[c] = Cartegories['Pavilion'][2]
#     pavilionDict4[d] = Cartegories['Pavilion'][3]
#     pavilionDict5[e] = Cartegories['Pavilion'][4]

# Specials
Specials = icra_specials[(icra_specials['Genre'] == 'Plenaries')
                         | (icra_specials['Genre'] == 'Keynotes')]
SpecialsSession = sorted(list(set(Specials['Genre'])))

# Workshops
Workshops = icra_workshops[(icra_workshops['Workshop Number'] == 20004) |
                           (icra_workshops['Workshop Number'] == 20008) |
                           (icra_workshops['Workshop Number'] == 20009) |
                           (icra_workshops['Workshop Number'] == 20014)]

WorkshopsSession = sorted(list(set(Workshops['Title'])))


#########################################################################################################
#########################################################################################################
#########################################################################################################
@csrf_exempt
def posttest(request):
    if request.is_ajax():
        print(request.POST['name'])

    return render(request, 'posttest.html')


# Login
def login(request):
    global iros2020_emailinput
    iros2020_emailinput = ''
    # dongbin1= []
    # for users in ieeeusers.objects.raw('SELECT * FROM polls_like'):
    #     dongbin = users.paperid
    #     dongbin1.append(dongbin)
    # print(dongbin1)
    # ieeeusers.objects.filter(ieeeusers_id='iros1').update(ieeeusers_password='gyuhozzang')
    # irosuser1 = Users(iros2020_name="Dongbin Kim", iros2020_email="dongbin.kim@unlv.edu")
    # irosuser2 = Users(iros2020_name="Dr. Paul Oh", iros2020_email="paul.oh@unlv.edu")
    # irosuser1.save()
    # irosuser2.save()
    # irosuser3 = Users(iros2020_name="Gyuho Lee", iros2020_email="leeg3@unlv.nevada.edu")
    # irosuser4 = Users(iros2020_name="Blake Hament", iros2020_email="blakehament@gmail.com")
    # irosuser3.save()
    # irosuser4.save()
    # for i in range(1553):
    #     db = Papers(paper_id=icra_example['Nr'][i])
    #     db.save()
    # print(len(icra_specials['Nr']))
    # for j in range(len(icra_specials['Nr'])):
    #     db1 = Papers(paper_id=icra_specials['Nr'][j])
    #     db1.save()
    # #
    # for k in range(len(icra_workshops['Workshop Number'])):
    #     db2 = Papers(paper_id=icra_workshops['Workshop Number'][k])
    #     db2.save()

    return render(request, './beta/1_login_beta.html')


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Main Page
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
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        result = binarySearch(iros2020registered_email, 0, len(iros2020registered_email) - 1, iros2020_emailinput)

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
                           'account': iros2020_emailinput,
                           'loginName': loginName
                           })
        else:
            return render(request, './beta/1-1_loginError_beta.html')


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Sessions : Pavilion, Specials, Workshops
def tvshow(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        selectedSession = request.GET['id']
        selectedPavilion = request.GET['id2']
        selectedPavilionNum = request.GET['id3']
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

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

        # Gold Sponsor Video
        goldSponsorSession = icra_sponsors[(icra_sponsors['Location'] == selectedSession)].reset_index()
        goldSponsorName = goldSponsorSession['Name'].reset_index()
        goldSponsorVideo = goldSponsorSession['Video'].reset_index()
        if request.method == "GET":
            paperLikeCount = []
            paperLikeButtonColor = []
            paperSaveButtonStatus = []
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
                                 PDFList['FN'], titleNumber['Nr'], paperLikeCount, paperLikeButtonColor, paperSaveButtonStatus)
            return render(request, './beta/3_pavilionSession_beta.html', {'Pavilion': selectedPavilion,
                                                                          'PavilionNum': selectedPavilionNum,
                                                                          'SessionList': selectedSessionList,
                                                                          'Session': selectedSession,
                                                                          'EpisodeContext': EpisodeContext,
                                                                          'account': iros2020_emailinput,
                                                                          'goldSponsorName': goldSponsorName['Name'],
                                                                          'goldSponsorVideo': goldSponsorVideo['Video'],
                                                                          'goldSponsorSession': goldSponsorSession[
                                                                              'Location'],
                                                                          })



def specials(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        selectedSpecial = request.GET['id']
        selectedGenre = request.GET['id2']
        specialEpisodeList = icra_specials[(icra_specials['Genre'] == selectedSpecial)]
        speakerName = specialEpisodeList['Speaker'].reset_index()
        speakerBiography = specialEpisodeList['Bio'].reset_index()
        specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
        specialEpisodeNumber = specialEpisodeList['Nr'].reset_index()

        specialLikeCount = []
        specialLikeButtonColor = []
        specialSaveButtonStatus = []

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

        specialEpisodeContext = zip(speakerName['Speaker'],
                                    speakerBiography['Bio'],
                                    specialEpisodeAbstract['Abstract'],
                                    specialEpisodeNumber['Nr'],specialLikeCount,specialLikeButtonColor,specialSaveButtonStatus
                                    )


        return render(request, './beta/3-1_plenariesSession_beta.html', {'selectedSpecial': selectedSpecial,
                                                                         'selectedGenre': selectedGenre,
                                                                         'specialEpisodeContext': specialEpisodeContext,
                                                                         'SpecialsSession': SpecialsSession,
                                                                         'account': iros2020_emailinput,
                                                                         })


def workshops(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        selectedWorkshops = request.GET['id']
        selectedGenre = request.GET['id2']
        workshopsEpisodeList = icra_workshops[(icra_workshops['Title'] == selectedWorkshops)].reset_index()
        workshopsHomepage = workshopsEpisodeList['Workshop Home Page'].iloc[0]
        workshopOrganizers = workshopsEpisodeList['Organizers'].iloc[0]
        workshopNumber = workshopsEpisodeList['Workshop Number'].iloc[0]


        Speaker = []
        for i in range(1, 15):
            if workshopsEpisodeList['Speaker ' + str(i)].iloc[0] == 'missing':
                break
            Speaker.append(workshopsEpisodeList['Speaker ' + str(i)].iloc[0])

        Institution = []
        for j in range(1, 15):
            if workshopsEpisodeList['Institution ' + str(j)].iloc[0] == 'missing':
                break
            Institution.append(workshopsEpisodeList['Institution ' + str(j)].iloc[0])

        TalkTitle = []
        for k in range(1, 15):
            if workshopsEpisodeList['Talk Title ' + str(k)].iloc[0] == 'missing':
                break
            TalkTitle.append(workshopsEpisodeList['Talk Title ' + str(k)].iloc[0])

        workshopEpisodeNumber = []
        for q in range(len(Speaker)):
            newNumb = int(workshopNumber)*100 + q
            workshopEpisodeNumber.append(newNumb)
        #
        # for q in range(len(Speaker)):
        #     newNumb = int(workshopNumber)*100 + q
        #     db2 = Papers(paper_id=newNumb)
        #     db2.save()
        #     print(newNumb)

        workshopLikeCount = []
        workshopLikeButtonColor = []
        workshopSaveButtonStatus = []
        for workshopNr in workshopEpisodeNumber:
            paper = get_object_or_404(Papers, paper_id=workshopNr)
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


        WorkshopsContext = zip(Speaker, Institution, TalkTitle, workshopEpisodeNumber, workshopLikeButtonColor, workshopLikeCount, workshopSaveButtonStatus)

        return render(request, './beta/3-2_workshopsSession_beta.html', {'selectedWorkshops': selectedWorkshops,
                                                                         'selectedGenre': selectedGenre,
                                                                         'WorkshopsContext': WorkshopsContext,
                                                                         'WorkshopsSession': WorkshopsSession,
                                                                         'workshopsHomepage': workshopsHomepage,
                                                                         'workshopOrganizers': workshopOrganizers,
                                                                         'account': iros2020_emailinput})


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Episodes : Pavilion, Specials, Workshops
def episode(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        selectedTitle = request.GET['id']
        selectedSession = request.GET['id2']

        findVideo = icra_example[(icra_example['Title'] == selectedTitle)]
        VideoList = findVideo['VID'].reset_index()
        selectedNumber = findVideo['Nr'].reset_index()
        suggestEpisodeNum = findSimilarTopic(selectedNumber['Nr'].iloc[0])

        similarPaper = icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[0]))]

        for i in range(1, 12):
            main2 = similarPaper.append(icra_example[(icra_example['Nr'] == int(suggestEpisodeNum[i]))])
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
        # print(SessionTitle)

        TitleList = similarPaper['Title'].reset_index()
        PDFList = similarPaper['FN'].reset_index()
        titleNumber = similarPaper['Nr'].reset_index()

        # Comments load area
        lengthComments = Comments.objects.filter(paper_id=selectedNumber['Nr'].iloc[0]).count()

        arrayComments = []
        for ac in range(lengthComments):
            arrayComments.append(Comments.objects.filter(paper_id=selectedNumber['Nr'].iloc[0])[ac].comment)

        paperLikeCount = []
        paperLikeButtonColor = []
        paperSaveButtonStatus = []


        if request.method == "GET":
            selectedPaper = get_object_or_404(Papers, paper_id=selectedNumber['Nr'].iloc[0])

            if current_account in selectedPaper.like_users.all():
                selectedPaperLikeButtonColor = 1
            else:
                selectedPaperLikeButtonColor = 0
            selectedPaperLikeCount = selectedPaper.like_users.count()

            if current_account in selectedPaper.save_users.all():
                selectedPaperbuttonStatus = 1
            else:
                selectedPaperbuttonStatus = 0

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
                             PDFList['FN'], titleNumber['Nr'], suggestEpisodeNum, paperLikeCount, paperLikeButtonColor, SessionTitle, paperSaveButtonStatus)
            return render(request, './beta/4_pavilionSessionEpisode_beta.html', {'VideoList': VideoList['VID'],
                                                                                 'Title': selectedTitle,
                                                                                 'Session': selectedSession,
                                                                                 'EpisodeContext': resultList,
                                                                                 'SelectedPaperNumber':
                                                                                     selectedNumber['Nr'].iloc[0],
                                                                                 'account': iros2020_emailinput,
                                                                                 'selectedPaperLikeButtonColor': selectedPaperLikeButtonColor,
                                                                                 'selectedPaperLikeCount': selectedPaperLikeCount,
                                                                                 'selectedPaperbuttonStatus':selectedPaperbuttonStatus,
                                                                                 'arrayComments':arrayComments,
                                                                                 'lengthComments':lengthComments})



def specialsepisode(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        # Selected Specials
        selectedSpeaker = request.GET['id']
        selectedSpecial = request.GET['id2']
        selectedGenre = request.GET['id3']
        findspeaker = icra_specials[(icra_specials['Speaker'] == selectedSpeaker)]
        specialVideo = findspeaker['Video'].reset_index()
        selectedSpecialNumber = findspeaker['Nr'].reset_index()

        # Other Specials
        specialEpisodeList = icra_specials[(icra_specials['Genre'] == selectedSpecial)]
        speakerName = specialEpisodeList['Speaker'].reset_index()
        speakerBiography = specialEpisodeList['Bio'].reset_index()
        specialEpisodeAbstract = specialEpisodeList['Abstract'].reset_index()
        specialEpisodeNumber = specialEpisodeList['Nr'].reset_index()

        # Comments load area
        lengthComments = Comments.objects.filter(paper_id=selectedSpecialNumber['Nr'].iloc[0]).count()
        arrayComments = []
        for ac in range(lengthComments):
            arrayComments.append(Comments.objects.filter(paper_id=selectedSpecialNumber['Nr'].iloc[0])[ac].comment)

        selectedSpecialLike = get_object_or_404(Papers, paper_id=selectedSpecialNumber['Nr'].iloc[0])

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

        specialEpisodeContext = zip(speakerName['Speaker'],
                                    speakerBiography['Bio'],
                                    specialEpisodeAbstract['Abstract'],
                                    specialEpisodeNumber['Nr'], specialLikeCount, specialLikeButtonColor, specialSaveButtonStatus
                                    )

        return render(request, './beta/4-1_plenariesSessionEpisode_beta.html', {'specialVideo': specialVideo['Video'],
                                                                                'selectedSpeaker': selectedSpeaker,
                                                                                'selectedSpecial': selectedSpecial,
                                                                                'selectedGenre': selectedGenre,
                                                                                'specialEpisodeContext': specialEpisodeContext,
                                                                                'selectedSpecialLikeCount':selectedSpecialLikeCount,
                                                                                'selectedSpecialLikeButtonColor':selectedSpecialLikeButtonColor,
                                                                                'selectedSpecialSaveButtonStatus':selectedSpecialSaveButtonStatus,
                                                                                'SelectedPaperNumber':
                                                                                    selectedSpecialNumber['Nr'].iloc[0],
                                                                                'arrayComments': arrayComments,
                                                                                'lengthComments': lengthComments,
                                                                                'account': iros2020_emailinput})


def workshopsepisode(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        selectedSpeaker = request.GET['id']
        selectedWorkshops = request.GET['id2']
        selectedGenre = request.GET['id3']
        selectedSpeakerNumber = request.GET['id4']

        findspeaker = icra_workshops[(icra_workshops['Speaker ' + str(selectedSpeakerNumber)] == selectedSpeaker)]
        workshopsVideo = findspeaker['Video ' + str(selectedSpeakerNumber)].reset_index()
        workshopsTalkTitle = findspeaker['Talk Title ' + str(selectedSpeakerNumber)].reset_index()
        workshopsEpisodeList = icra_workshops[(icra_workshops['Title'] == selectedWorkshops)].reset_index()
        workshopNumber = workshopsEpisodeList['Workshop Number'].iloc[0]

        Speaker = []
        for i in range(1, 15):
            if workshopsEpisodeList['Speaker ' + str(i)].iloc[0] == 'missing':
                break
            Speaker.append(workshopsEpisodeList['Speaker ' + str(i)].iloc[0])

        Institution = []
        for j in range(1, 15):
            if workshopsEpisodeList['Institution ' + str(j)].iloc[0] == 'missing':
                break
            Institution.append(workshopsEpisodeList['Institution ' + str(j)].iloc[0])

        TalkTitle = []
        for k in range(1, 15):
            if workshopsEpisodeList['Talk Title ' + str(k)].iloc[0] == 'missing':
                break
            TalkTitle.append(workshopsEpisodeList['Talk Title ' + str(k)].iloc[0])

        workshopEpisodeNumber = []
        for q in range(len(Speaker)):
            newNumb = int(workshopNumber) * 100 + q
            workshopEpisodeNumber.append(newNumb)

        selectedWorkshopEpisodeNumber = int(workshopNumber) * 100 + int(selectedSpeakerNumber) - 1

        # Comments load area
        lengthComments = Comments.objects.filter(paper_id=selectedWorkshopEpisodeNumber).count()
        arrayComments = []
        for ac in range(lengthComments):
            arrayComments.append(Comments.objects.filter(paper_id=selectedWorkshopEpisodeNumber)[ac].comment)

        # Selected Workshop Like, MyList
        selectedWorkshopLike = get_object_or_404(Papers, paper_id=selectedWorkshopEpisodeNumber)

        if current_account in selectedWorkshopLike.like_users.all():
            selectedWorkshopLikeButtonColor = 1
        else:
            selectedWorkshopLikeButtonColor = 0
        selectedWorkshopLikeCount = selectedWorkshopLike.like_users.count()

        if current_account in selectedWorkshopLike.save_users.all():
            selectedWorkshopSaveButtonStatus = 1
        else:
            selectedWorkshopSaveButtonStatus = 0

        # Other Workshops Like
        workshopLikeCount = []
        workshopLikeButtonColor = []
        workshopSaveButtonStatus = []

        for workshopNr in workshopEpisodeNumber:
            paper = get_object_or_404(Papers, paper_id=workshopNr)
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

        WorkshopsContext = zip(Speaker, Institution, TalkTitle, workshopEpisodeNumber, workshopLikeButtonColor,
                               workshopLikeCount, workshopSaveButtonStatus)

        return render(request, './beta/4-2_workshopsSessionEpisode_beta.html',
                      {'workshopsVideo': workshopsVideo['Video ' + str(selectedSpeakerNumber)],
                       'workshopsTalkTitle': workshopsTalkTitle['Talk Title ' + str(selectedSpeakerNumber)],
                       'selectedSpeaker': selectedSpeaker,
                       'selectedWorkshops': selectedWorkshops,
                       'selectedGenre': selectedGenre,
                       'WorkshopsContext': WorkshopsContext,
                       'account': iros2020_emailinput,
                       'SelectedPaperNumber':selectedWorkshopEpisodeNumber,
                       'selectedWorkshopLikeButtonColor':selectedWorkshopLikeButtonColor,
                       'selectedWorkshopLikeCount':selectedWorkshopLikeCount,
                       'selectedWorkshopSaveButtonStatus':selectedWorkshopSaveButtonStatus,
                       'arrayComments': arrayComments,
                       'lengthComments': lengthComments,
                       })



#########################################################################################################
#########################################################################################################
#########################################################################################################
# Search Results
def searchresult(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        inputKeyword = request.GET['id']
        resultNumber = searchByKeyword(inputKeyword)
        resultNumberlength = len(resultNumber)

        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        if not resultNumber:
            return render(request, './beta/6_searchResultError_beta.html', {'inputKeyword': inputKeyword})
        else:
            searchTitle = icra_example[(icra_example['Nr'] == int(resultNumber[0]))]

            for i in range(1, resultNumberlength):
                main2 = searchTitle.append(icra_example[(icra_example['Nr'] == int(resultNumber[i]))])
                searchTitle = main2

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

            paperLikeCount = []
            paperLikeButtonColor = []
            paperSaveButtonStatus = []

            if request.method == "GET":

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
                                 PDFList['FN'], titleNumber['Nr'], paperLikeCount, paperLikeButtonColor, paperSaveButtonStatus, SessionList['Session title'])

            return render(request, './beta/5_searchResult_beta.html', {'EpisodeContext': resultList,
                                                                       'account': iros2020_emailinput})


#########################################################################################################
#########################################################################################################
#########################################################################################################

# My List
def mylist(request):
    global iros2020_emailinput

    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        user = get_object_or_404(Users, iros2020_email=iros2020_emailinput)
        mylistQuery = user.save_papers.all()
        mylistNumber = mylistQuery.count()

        #Arrange Numbers by Genres
        mylistEpisodeNumber = []
        mylistSpecialNumber = []
        mylistWorkshopsNumber = []
        for i in range(mylistNumber):
            if mylistQuery[i].paper_id < 10000:
                mylistEpisodeNumber.append(mylistQuery[i].paper_id)
            elif mylistQuery[i].paper_id < 20000:
                mylistSpecialNumber.append(mylistQuery[i].paper_id)
            else:
                mylistWorkshopsNumber.append(mylistQuery[i].paper_id)

        # MyList Episodes
        if len(mylistEpisodeNumber) != 0:
            mylistEpisodeTitle = []
            mylistEpisodeSession = []
            for i in range(len(mylistEpisodeNumber)):
                mylistEpisode = icra_example[(icra_example['Nr'] == int(mylistEpisodeNumber[i]))].reset_index()
                mylistEpisodeSession.append(mylistEpisode['Session title'].iloc[0])
                mylistEpisodeTitle.append(mylistEpisode['Title'].iloc[0])

            mylistEpisodeContext = zip(mylistEpisodeTitle, mylistEpisodeSession)
        else:
            mylistEpisodeContext = []


        # MyList Specials
        if len(mylistSpecialNumber) != 0:

            mylistSpecialSpeaker = []
            mylistSpecialSpecial = []
            mylistSpecialGenre = []
            for j in range(len(mylistSpecialNumber)):
                mylistSpecial = icra_specials[(icra_specials['Nr'] == int(mylistSpecialNumber[j]))].reset_index()
                mylistSpecialSpeaker.append(mylistSpecial['Speaker'].iloc[0])
                mylistSpecialSpecial.append(mylistSpecial['Genre'].iloc[0])
                mylistSpecialGenre.append('Specials')

            mylistSpecialContext = zip(mylistSpecialSpeaker, mylistSpecialSpecial, mylistSpecialGenre)
        else:
            mylistSpecialContext = []

        # MyList Workshops
        if len(mylistWorkshopsNumber) != 0:
            workshopNumber = []
            speakerNumber = []
            for q in mylistWorkshopsNumber:
                workshopNumber.append(math.trunc(q/100))
                speakerNumber.append(q - math.trunc(q/100)*100 + 1)

            mylistWorkshopsSpeaker = []
            mylistWorkshopsWorkshop = []
            mylistWorkshopsGenre = []
            mylistWorkshopsSpeakerNumber = speakerNumber
            mylistWorkshopsTalkTitle = []
            for w in range(len(mylistWorkshopsNumber)):
                mylistWorkshops = icra_workshops[(icra_workshops['Workshop Number'] == workshopNumber[w])].reset_index()
                mylistWorkshopsSpeaker.append(mylistWorkshops['Speaker ' + str(speakerNumber[w])].iloc[0])
                mylistWorkshopsWorkshop.append(mylistWorkshops['Title'].iloc[0])
                mylistWorkshopsGenre.append('Workshops')
                mylistWorkshopsTalkTitle.append(mylistWorkshops['Talk Title ' + str(speakerNumber[w])].iloc[0])

            mylistWorkshopsContext = zip(mylistWorkshopsSpeaker, mylistWorkshopsWorkshop, mylistWorkshopsGenre, mylistWorkshopsSpeakerNumber, mylistWorkshopsTalkTitle)
        else:
            mylistWorkshopsContext = []


        return render(request, './beta/7_myList_beta.html', {'account': iros2020_emailinput,
                                                             'mylistEpisodeNumber':len(mylistEpisodeNumber),
                                                             'mylistEpisodeContext':mylistEpisodeContext,
                                                             'mylistSpecialNumber':len(mylistSpecialNumber),
                                                             'mylistSpecialContext':mylistSpecialContext,
                                                             'mylistWorkshopsNumber':len(mylistWorkshopsNumber),
                                                             'mylistWorkshopsContext':mylistWorkshopsContext,
                                                             })


#########################################################################################################
#########################################################################################################
#########################################################################################################
# Like Function
@csrf_exempt
def post_like(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        paperLikeCount = []

        if request.is_ajax:
            clickedPaperNumber = int(request.POST['paperNumber'])
            paper = get_object_or_404(Papers, paper_id=clickedPaperNumber)

            if current_account in paper.like_users.all():
                paper.like_users.remove(current_account)
                buttonColor = "grey"
            else:
                paper.like_users.add(current_account)
                buttonColor = "yellow"

            paperLikeCount.append(paper.like_users.count())
            response = {'likeButtonColor': buttonColor, 'likeCount': paperLikeCount}

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )

@csrf_exempt
def add_comment(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)
        # print(current_account)
        # Comments load area
        if request.is_ajax:
            clickedPaperNumber = int(request.POST['paperNumber'])
            c1 = Comments(paper_id=clickedPaperNumber, comment= request.POST['comment'])
            c1.save()
            c1.comment_users.add(current_account)

            lengthComments = Comments.objects.filter(paper_id=clickedPaperNumber).count()

            response = {'commentAdded': str(lengthComments) + " : " + request.POST['comment'],'lengthComments':lengthComments}

        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )

@csrf_exempt
def post_save(request):
    global iros2020_emailinput
    if iros2020_emailinput == '':
        return render(request, './beta/1-1_loginError_beta.html')
    else:
        current_account = iros2020registered_db.get(iros2020_email=iros2020_emailinput)

        if request.is_ajax:
            clickedPaperNumber = int(request.POST['paperNumber'])
            paper = get_object_or_404(Papers, paper_id=clickedPaperNumber)

            if current_account in paper.save_users.all():
                paper.save_users.remove(current_account)
                buttonStatus = 'fa fa-plus'
            else:
                paper.save_users.add(current_account)
                buttonStatus = 'fa fa-check-circle'

            response = {'paperSaveButtonStatus': buttonStatus}

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )