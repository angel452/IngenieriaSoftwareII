from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from pixelsaurapp.models import Category


@login_required
def dashboard(request):
    categories = Category.objects.all()
    return render(request, 'account/dashboard.html',{'categories': categories,'section': 'dashboard'})

def user_login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        ' successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'categories': categories,'form': form})

def outview(request):
    categories = Category.objects.all()
"""
def logoutview(request):
    categories = Category.objects.all()
    return()


""" 