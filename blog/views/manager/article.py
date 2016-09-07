# coding:utf-8
from datetime import date
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import Storage, FileSystemStorage
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from blog.lib.expaginator import ExPaginator
from blog.models import Article, Column

@login_required(login_url='admin_login')
def showArticles(request):
    articles = Article.objects.all()
    paginator = ExPaginator(articles,2)
    pageNumber = request.GET.get('pageNumber')
    try:
        page = paginator.page(pageNumber)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request,'manager/article/showArticles.html',{'page':page})

@login_required(login_url='admin_login')
def editArticle(request):
    # 获得所有的栏目和用户名，用在后面的页面里的下拉选择
    columns = Column.objects.all()
    users = User.objects.all()

     # 根据是否是post判断市显示编辑页面还是执行编辑操作
    if request.method == 'POST':
        # 获得表单提交数据
        articleId = request.POST.get('articleId')
        articleName = (request.POST.get('articleName')).strip()
        articleColumnId = request.POST.get('articleColumn')
        atrticleUserId = request.POST.get('atricleUser')
        articlePic = request.FILES.get('articlePic')
        articleCount = request.POST.get('articleCount')
        # 验证
        if articleName == '':
            return render(request,'manager/article/editArticle.html',{'note':'文章名称不能为空'})

        article = Article.objects.get(pk=articleId)
        # 获得要删除文件的路径
        delpath = ''
        if article.articlepic != '':
            delpath = article.articlepic.path

        # 更新文章
        article.articlename = articleName
        article.articlecolumn = Column.objects.get(pk=articleColumnId)
        article.articleuser = User.objects.get(pk=atrticleUserId)
        article.articletime = date.today()
        article.articlepic = articlePic
        article.articlecontent = articleCount
        article.save()

        # 删除修改后不需要的文件
        if delpath !='':
            fs = FileSystemStorage()
            fs.delete(delpath)
        return HttpResponseRedirect(reverse('admin_article_show'))
    else:
        articleId = request.GET.get('articleId')
        article = Article.objects.get(pk=articleId)
        return render(request,'manager/article/editArticle.html',{'article':article,'columns':columns,'users':users})

@login_required(login_url='admin_login')
def addArticle(request):
    columns = Column.objects.all()
    users = User.objects.all()
    if request.method !='POST':
        return render(request,'manager/article/addArticle.html',{'columns':columns,'users':users})
    else:

        # 获得数据
        articleName = (request.POST.get('articleName')).strip()
        articlecolumnId = request.POST.get('articleColumn')
        articleuserId = request.POST.get('atricleAuthor')
        articleImg = request.FILES.get('articleImg')
        articleCount = request.POST.get('atricleCount')
        print articleImg
        # 验证
        if articleName == '':
            return render(request,'manager/article/addArticle.html',{'columns':columns,'users':users,'note':'文章名称不能为空'})
        elif articlecolumnId == 0:
            return render(request,'manager/article/addArticle.html',{'columns':columns,'users':users,'note':'请选择文章分类'})
        elif articleuserId == 0:
            return render(request,'manager/article/addArticle.html',{'columns':columns,'users':users,'note':'请选择文章作者'})
        # 保存文章
        article = Article()
        article.articlename = articleName
        article.articleuser = User.objects.get(pk=articleuserId)
        article.articlecolumn = Column.objects.get(pk=articlecolumnId)
        article.articlepic = articleImg
        article.articletime = date.today()
        article.articlecontent = articleCount
        article.save()
        return HttpResponseRedirect(reverse('admin_article_show'))

# 删除文章操作
@login_required(login_url='admin_login')
def delArticle(request):
    articleId = request.GET.get('articleId')
    article = Article.objects.get(pk = articleId)
    # 删除图片
    if article.articlepic != '':
        fs = FileSystemStorage()
        fs.delete(article.articlepic.path)

    # 删除文章
    article.delete()
    return HttpResponseRedirect(reverse('admin_article_show'))