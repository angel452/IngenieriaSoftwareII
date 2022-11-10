from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # post views
    #path('login/', views.user_login, name='account_login'), #previous login
    path('login/', auth_views.LoginView.as_view(), name='login'),  #this name: login have to put in settings.py 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  #this name: logout have to put in settings.py 
    path('', views.dashboard, name='dashboard')  #this name: dashboard have to put in settings.py 
]