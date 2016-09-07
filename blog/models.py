# coding:utf-8
from __future__ import unicode_literals
import datetime

from django.db import models

# Create your models here.
from myapp.settings import MEDIA_ROOT


class Column(models.Model):
    columnname = models.CharField('栏目',max_length=100)

class Article(models.Model):
    articlename = models.CharField('文章名称',max_length=100)
    articleuser = models.ForeignKey('auth.User',blank=True,null=True,verbose_name='作者')
    articlepic = models.FileField(upload_to='imgs/%Y/%m/%d')
    articlecolumn = models.ForeignKey('Column',verbose_name='栏目')
    articletime = models.DateField('文章日期')
    articlecontent = models.TextField('文章内容')

