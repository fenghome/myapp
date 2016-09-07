from django.shortcuts import render

__author__ = 'lenovo'
def index(request):
    return render(request,'blog/Index/index.html')