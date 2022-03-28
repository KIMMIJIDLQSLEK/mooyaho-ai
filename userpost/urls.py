from django.urls import path
from . import views

urlpatterns=[
    path('userpost', views.userpost , name='userpost'),
]
