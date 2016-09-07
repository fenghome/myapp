"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from blog.views.blog import index as blogIndex,article as blogArticle
from blog.views.manager import index, users, column, article, account

urlpatterns = [

    url(r'^$', blogIndex.index, name='blog_index'),
    url(r'^article/$', blogArticle.index, name='blog_article'),


    url(r'^admin/login/$', account.userlogin, name='admin_login'),
    url(r'^admin/logout/$', account.userlogout, name='admin_logout'),
    url(r'^admin/changepas/$', account.changepassword, name='admin_changepas'),

    url(r'^admin/$', index.index, name='admin_index'),
    url(r'^admin/head/$', index.head, name='admin_index_head'),
    url(r'^admin/left/$', index.left, name='admin_index_left'),
    url(r'^admin/right/$', index.right, name='admin_index_right'),

    url(r'^admin/users/show/$', users.showUser, name='admin_users_show'),
    url(r'^admin/users/edit/$', users.editUser, name='admin_users_edit'),
    url(r'^admin/users/add/$', users.addUser, name='admin_users_add'),
    url(r'^admin/users/del/$', users.delUser, name='admin_users_del'),

    url(r'^admin/column/show/$', column.showColumn, name='admin_column_show'),
    url(r'^admin/column/edit/$', column.editColumn, name='admin_column_edit'),
    url(r'^admin/column/add/$', column.addColumn, name='admin_column_add'),
    url(r'^admin/column/del/$', column.delColumn, name='admin_column_del'),

    url(r'^admin/article/show/$', article.showArticles, name='admin_article_show'),
    url(r'^admin/article/edit/$', article.editArticle, name='admin_article_edit'),
    url(r'^admin/article/add/$', article.addArticle, name='admin_article_add'),
    url(r'^admin/article/del/$', article.delArticle, name='admin_article_del'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
