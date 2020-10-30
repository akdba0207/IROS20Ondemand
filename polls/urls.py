from django.conf.urls import url
from django.urls import path, re_path,include
from polls import views

urlpatterns = [
    path('', views.login, name='login_main'),
    path('logout',views.logout,name='logout_main'),
    path('signup', views.signup, name='signup_main'),
    path('resendactivation', views.resendactivation, name='resendactivation_main'),
    re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent_main'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate_main'),

    path('entrance',views.entrance,name='entrance_main'),
    path('main', views.main, name='main'),
    path('tvshow', views.tvshow),
    path('specials', views.specials),
    path('workshops', views.workshops),
    path('episode', views.episode),
    path('specialsepisode',views.specialsepisode),
    path('workshopsepisode', views.workshopsepisode),
    path('searchresult',views.searchresult),
    path('mylist',views.mylist),
    path('post_like', views.post_like, name='post_like'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('post_save', views.post_save, name='post_save'),
    path('post_hitcount', views.post_hitcount, name='post_hitcount'),

    path('update_playtime', views.update_playtime, name='update_playtime'),
    path('competition', views.competition),
    path('about',views.about),
    path('faqhelp',views.faqhelp),
    path('partners',views.partners),
    path('partnerspage',views.partnerspage),
    path('placeyourads',views.placeyourads),
    url(r'session_security/', include('session_security.urls')),
    path('save_last_activity', views.save_last_activity, name='save_last_activity'),

    # path('post_like', views.post_like, name='post_like'),
    # path('add_comment', views.add_comment, name='add_comment'),
    # path('post_save', views.post_save, name='post_save'),
    # path('post_hitcount', views.post_hitcount, name='post_hitcount'),
]