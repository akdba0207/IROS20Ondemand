from django.urls import path

from . import views

urlpatterns = [
    path('tvshow', views.tvshow),
    path('episode', views.episode),
    path('', views.main),
]