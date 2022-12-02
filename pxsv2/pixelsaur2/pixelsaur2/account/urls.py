from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy, path, include

app_name = 'account'


#direcciones para el movimiento de login - logout
urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(), name='login'),  #this name: login have to put in settings.py 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  #this name: logout have to put in settings.py 
   

    # ---------- For changin passwords ---------------
    path('password_change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('account:password_change_done')
                                                                ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # ------------------- Resseting password view ----------------------
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('account:password_reset_done')
                                                                ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('account:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),

    # -------------------- Register new user -------------------------------
    path('register/', views.register, name='register'),
]