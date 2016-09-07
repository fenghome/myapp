# coding:utf-8
from django.shortcuts import render

def index(request):
    render(request,'blog/Article/index.html')