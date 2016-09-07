# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

__author__ = 'lenovo'

@login_required(login_url='admin_login')
def index(request):
    return render(request, 'manager/index/index.html')

@login_required(login_url='admin_login')
def head(request):
    if request.user.is_authenticated():
        username=request.user.username
    else:
        username=''
    return render(request, 'manager/index/head.html',{'username':username})

@login_required(login_url='admin_login')
def left(request):
    return render(request, 'manager/index/left.html')

@login_required(login_url='admin_login')
def right(request):
    return render(request, 'manager/index/right.html')
