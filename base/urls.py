"""URLS file for the base application"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="HomePage"),
    path('job/<str:pk>/', views.job, name="Job"),
    path('create-job-listing/', views.addJob, name='add-job'),
    path('update-job-listing/<str:pk>/', views.updateJob, name='update-job'),
    path('delete-job-listing/<str:pk>/', views.deleteJob, name='delete-job'),
]
