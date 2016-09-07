# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from blog.lib.expaginator import ExPaginator
from blog.models import Column
@login_required(login_url='admin_login')
def showColumn(request):
    columns = Column.objects.all()
    paginator = ExPaginator(columns,2)
    pageNumber = request.GET.get('pageNumber')
    try:
        page = paginator.page(pageNumber)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request,'manager/column/showColumn.html',{'page':page})

@login_required(login_url='admin_login')
def editColumn(request):
    if request.method != 'POST':
        columnname = request.GET.get('colName')
        return render(request,'manager/column/editColumn.html',{'colName':columnname,'oldName':columnname})
    else:
        columnname = request.POST.get('colName')
        oldcolname = request.POST.get('oldName')
        if columnname == '':
            return render(request,'manager/column/editColumn.html',{'colName':columnname,'oldName':columnname,'note':'栏目不能为空'})
        elif columnname != oldcolname and len(Column.objects.filter(columnname=columnname))>0:
            return render(request,'manager/column/editColumn.html',{'colName':columnname,'oldName':columnname,'note':'栏目已经存在'})

        column = Column.objects.get(columnname=oldcolname)
        column.columnname = columnname
        column.save()
        return HttpResponseRedirect(reverse('admin_column_show', args=()))

@login_required(login_url='admin_login')
def addColumn(request):
    # 确定是显示增加栏目页面还是增加栏目的逻辑操作
    if request.method != 'POST':
        return render(request,'manager/column/addColumn.html')
    else:
        columnName = (request.POST.get('colName')).strip()
        # 数据校验
        if columnName == '':
            return render(request,'manager/column/addColumn.html',{'note':'栏目不能为空'})
        elif len(Column.objects.filter(columnname = columnName))>0:
            return render(request,'manager/column/addColumn.html',{'note':'栏目已经存在'})

        # 添加栏目
        column = Column(columnname=columnName)
        column.save()
        return HttpResponseRedirect(reverse('admin_column_show', args=()))

@login_required(login_url='admin_login')
def delColumn(request):
    columnname = request.GET.get('colName')
    column = Column.objects.get(columnname=columnname)
    # 如果栏目下有文章不能删除栏目
    if column.article_set.count() != 0:
        return HttpResponse("<script language='JavaScript'>alert('该栏目有发表的文章，请先删除发表的文章');self.location='/admin/column/show/';</script>")

    column.delete()
    return HttpResponseRedirect(reverse('admin_column_show'))