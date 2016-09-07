# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.lib.expaginator import ExPaginator

__author__ = 'lenovo'

@login_required(login_url='admin_login')
def showUser(request):
    users = User.objects.all()
    paginator = ExPaginator(users,2)
    pageNumber = request.GET.get('pageNumber')
    try:
        page = paginator.page(pageNumber)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request,'manager/users/showUser.html',{'page':page})

@login_required(login_url='admin_login')
def editUser(request):
    # 判断确定是显示编辑界面还是进行编辑用户的逻辑操作
    if request.method == 'POST':
        username = (request.POST.get('username')).strip()
        userpassword = (request.POST.get('userpass')).strip()
        oldusername = (request.POST.get('oldname')).strip()

        # 有效性判断
        if username == '':
            return render(request,'manager/users/editUser.html',{'username':username,'oldname':oldusername,'note':'用户名不能为空'})
        elif userpassword == '':
            return render(request,'manager/users/editUser.html',{'username':username,'oldname':oldusername,'note':'密码不能为空'})
        elif username != oldusername and len(User.objects.filter(username=username))>0:
            return render(request,'manager/users/editUser.html',{'username':username,'oldname':oldusername,'note':'用户名已经存在'})

        #存储修改后的用户名和密码
        user = User.objects.get(username=oldusername)
        user.username = username
        user.set_password(userpassword)
        user.save()
        return HttpResponseRedirect(reverse('admin_users_show'))
    #显示编辑用户名界面
    else:
        username = request.GET.get('username')
        return render(request,'manager/users/editUser.html',{'username':username,'oldname':username})

@login_required(login_url='admin_login')
def addUser(request):
    note = ''
    if request.method == 'POST':
        username = str(request.POST.get('username')).strip()
        userpassword = str(request.POST.get('userpass')).strip()
        userrepass = str(request.POST.get('userrepass')).strip()

        if username =='':
            note = '用户名不能为空'
        elif userpassword == '':
            note = '密码不能为空'
        elif userpassword != userrepass:
            note = '两次输入的密码不一致'
        else:
            user = User.objects.filter(username = username)
            if len(user) != 0:
                note = '用户名已经存在'
            else:
                user = User.objects.create_user(username = username,password=userpassword)
                user.save()
                return HttpResponseRedirect(reverse('admin_users_show', args=()))
    return render(request,'manager/users/addUser.html',{'note':note})

@login_required(login_url='admin_login')
def delUser(request):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    if user.article_set.count()!=0:
         return HttpResponse("<script language='JavaScript'>alert('该用户有发表的文章，请先删除发表的文章');self.location='/admin/users/show/';</script>")
    else:
        user.delete()
        return HttpResponseRedirect(reverse('admin_users_show'))

