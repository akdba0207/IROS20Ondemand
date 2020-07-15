from django.urls import path

from . import views

urlpatterns = [
    path('tvshow', views.tvshow),
    path('episode', views.episode),
    path('searchresult',views.searchresult),
    path('suggestion', views.suggestion),
    path('', views.main),
]