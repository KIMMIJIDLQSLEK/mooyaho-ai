from django.urls import path
from . import views

urlpatterns=[
    path('userviewlog', views.userviewlog , name='userviewlog'),
]
