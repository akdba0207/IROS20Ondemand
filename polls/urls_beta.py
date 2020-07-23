from django.urls import path

from . import views_beta

urlpatterns = [
    path('tvshow', views_beta.tvshow),
    path('episode', views_beta.episode),
    path('searchresult',views_beta.searchresult),
    path('suggestion', views_beta.suggestion),
    path('', views_beta.main),
]