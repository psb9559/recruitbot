from django.urls import path
from . import views

#app_name='wonbot'
urlpatterns = [
    #re_path(r'^$', views.index),
    #path('', views.keyboard, name='keyboard'),
    path('', views.message, name = 'message'),
             
 
 
]
 
