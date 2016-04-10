from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^recommend/', views.friends_list, name='friend_list'),
]