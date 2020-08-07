from django.urls import path

from . import views_beta

urlpatterns = [
    path('tvshow', views_beta.tvshow),
    path('episode', views_beta.episode),
    path('searchresult',views_beta.searchresult),
    path('suggestion', views_beta.suggestion),
    path('', views_beta.login),
    path('mylist',views_beta.mylist),
    path('specials',views_beta.specials),
    path('specialsepisode',views_beta.specialsepisode),
    path('workshops', views_beta.workshops),
    path('workshopsepisode', views_beta.workshopsepisode),
    path('main', views_beta.main),
    # path('posttest', views_beta.posttest, name='posttest')
    path('post_like', views_beta.post_like, name='post_like')
]