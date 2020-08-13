from django.urls import path

from . import views_beta

urlpatterns = [
    path('', views_beta.login),
    path('main', views_beta.main),
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
    path('post_hitcount', views_beta.post_hitcount, name='post_hitcount')
]