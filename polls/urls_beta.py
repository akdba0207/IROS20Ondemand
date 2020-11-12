# * Copyright (C) Dongbin Kim - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Dongbin Kim <akdba0207@gmail.com>, September, 2020
from django.conf.urls import url
from django.urls import path, re_path, include
from polls import views_beta

from . import views_beta

urlpatterns = [
    path('', views_beta.login, name='login'),
    path('logout',views_beta.logout,name='logout'),
    path('entrance',views_beta.entrance,name='entrance'),
    path('main', views_beta.main, name='main'),
    path('tvshow', views_beta.tvshow),
    path('specials', views_beta.specials),
    path('workshops', views_beta.workshops),
    path('episode', views_beta.episode),
    path('specialsepisode',views_beta.specialsepisode),
    path('workshopsepisode', views_beta.workshopsepisode),
    path('searchresult',views_beta.searchresult),
    path('mylist',views_beta.mylist),
    path('post_like', views_beta.post_like, name='post_like'),
    path('add_comment', views_beta.add_comment, name='add_comment'),
    path('post_save', views_beta.post_save, name='post_save'),
    path('post_hitcount', views_beta.post_hitcount, name='post_hitcount'),
    path('signup', views_beta.signup, name='signup'),
    path('resendactivation', views_beta.resendactivation, name='resendactivation'),
    path('update_playtime', views_beta.update_playtime, name='update_playtime'),
    path('competition',views_beta.competition),
    path('about',views_beta.about),
    path('faqhelp',views_beta.faqhelp),
    path('partners',views_beta.partners),
    path('partnerspage',views_beta.partnerspage),
    path('placeyourads',views_beta.placeyourads),
    path('jobs',views_beta.jobs),

    re_path(r'^account_activation_sent/$', views_beta.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views_beta.activate, name='activate'),
    # path('activate/<str:uid64>/<str:token>/',views_beta.activate, name='activate'),

    url(r'session_security/', include('session_security.urls')),
    path('save_last_activity', views_beta.save_last_activity, name='save_last_activity'),
]