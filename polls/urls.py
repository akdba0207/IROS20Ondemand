from django.urls import path

from . import views

urlpatterns = [
    path('tvshow', views.tvshow),
    path('episode', views.episode),
    path('searchresult',views.searchresult),
    path('suggestion', views.suggestion),
    path('login', views.login),
    path('mylist',views.mylist),
    path('specials',views.specials),
    path('specialsepisode',views.specialsepisode),
    path('workshops', views.workshops),
    path('workshopsepisode', views.workshopsepisode),
    path('', views.main),
]