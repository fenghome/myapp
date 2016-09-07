# coding:utf-8
from django.core.paginator import Paginator
__author__ = 'Administrator'
class ExPaginator(Paginator):

    #重载了一下，添加了一个range_num参数，表示一次显示的分页范围，默认为一次显示10页
    def __init__(self, object_list, per_page,range_num=10, orphans=0,allow_empty_first_page=True):
        self.range_num =range_num
        Paginator.__init__(self, object_list, per_page, orphans=0,allow_empty_first_page=True)

    #重载了一下，得到当前页curpafe
    def page(self, number):
        self.curpage = number
        return super(ExPaginator,self).page(number)

    #新定义方法，一次显示部分分页。
    def _page_range_ext(self):
        #根据当前页和每一次显示的页码数相比较，计算出当前分页范围的最小分页值和最大分页值。
        if float(self.curpage) % self.range_num == 0:
            min_range_page = (int(float(self.curpage)/self.range_num)-1)*self.range_num+1
        else:
            min_range_page = int(float(self.curpage)/self.range_num)*self.range_num+1
        max_range_page = min_range_page + self.range_num
        pagerange_all = list(super(ExPaginator,self)._get_page_range())
        pagerange_alittle = range(min_range_page,max_range_page)
        pagerange = list(set(pagerange_all).intersection(set(pagerange_alittle)))
        return pagerange
    page_range_ext = property(_page_range_ext)


