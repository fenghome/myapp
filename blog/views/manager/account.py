# coding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def userlogin(request):
    # 判断是执行登录逻辑操作还是现实登录页面
    if request.method == 'POST':
        # 认证判断
        username = request.POST.get('username')
        password = request.POST.get('userpass')
        print username
        print password
        user = authenticate(username=username, password=password)
        # 登入用户
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('admin_index'))
            else:
                return render(request,'manager/account/login.html',{'tishi':'不是该用户，请重新登录'})
        else:
             return render(request,'manager/account/login.html',{'tishi':'不是该用户，请重新登录'})
    else:
        return render(request,'manager/account/login.html')

def userlogout(request):
    logout(request)
    return HttpResponse("<script language='JavaScript'>alert('退出成功');self.location='/admin/';</script>")

def changepassword(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            oldpaw = (request.POST.get('oldpaw')).strip()
            newpaw = (request.POST.get('newpaw')).strip()
            if oldpaw == '':
                return render(request,'manager/account/changepaw.html',{'tishi':'旧密码不能为空'})
            elif newpaw == '':
                return render(request,'manager/account/changepaw.html',{'tishi':'新密码不能为空'})
            user = request.user
            if not user.check_password(oldpaw):
                return render(request,'manager/account/changepaw.html',{'tishi':'旧密码错误'})
            user.set_password(newpaw)
            user.save()
            return HttpResponse("<script language='JavaScript'>parent.location='/admin/';</script>")
    else:
        return render(request,'manager/account/changepaw.html')