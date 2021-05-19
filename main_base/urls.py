from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('user/', views.userpage, name = "user"),
    path('registration/', views.registration, name = "registration"),
    path('login/', views.loginUser, name = "login"),
    path('employeelist/', views.employeelist, name = "employeelist"),
    path('userdetails/', views.userdetails, name = "userdetails"),
    path('messageadmin/', views.messageadmin, name = "messageadmin"),
    path('user_details/', views.user_details, name = "user_details"),
    path('attendance/', views.TakeAttendance, name = "attendance"),
    path('submit/', views.RecognitionSubmit, name = "submit"),
    path('logout/', views.logoutUser, name = "logout"),
]