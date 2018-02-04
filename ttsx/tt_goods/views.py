from django.shortcuts import render
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator,Page
from .models import *
from django.http import HttpResponse
# Create your views here.
def index(request):
    '''
    原则：模板中需要的数据，就从视图中传递过去
    需要的数据包括：分类，3个最热商品，4个最新商品{type:t,hot:[],new:[]}
    共六个分类：[{},{},{}...]
    '''
    goods=[]
    tlist=TypeInfo.objects.all()
    for t in tlist:
        dict={'type':t}
        #查询当前分类最热门的3个商品
        dict['hot']=t.goodsinfo_set.all().order_by('-gclick')[0:3]
        #查询当前分类最新的4个商品
        dict['new']=GoodsInfo.objects.filter(gtype=t).order_by('-id')[0:4]
        #将数据构造列表，用于传递到模板中
        goods.append(dict)
    context={'isCart':1,'goods':goods}
    return render(request,'tt_goods/index.html',context)


def list(request,tid,pindex,order):
    '''
    模板需要的数据：分类名称，最新的2个，当前页的数据
    排序：1是默认，2是价格升序，3是价格降序，4是最火
    '''
    #指定排序规则
    order_str='-id'
    if order=='2':
        order_str='gprice'
    elif order=='3':
        order_str='-gprice'
    elif order=='4':
        order_str='-gclick'
    #获取分类对象
    t=TypeInfo.objects.get(id=tid)
    #获取最新的2个
    new=t.goodsinfo_set.all().order_by('-id')[0:2]
    #当前分类的所有商品
    glist=GoodsInfo.objects.filter(gtype_id=tid).order_by(order_str)
    #分页
    paginator=Paginator(glist,10)
    #验证当前页码的合法性
    pindex=int(pindex)
    if pindex<=1:
        pindex=1
    if pindex>=paginator.num_pages:
        pindex=paginator.num_pages
    #获取当前页的数据
    page=paginator.page(pindex)
    #构造页码列表
    if paginator.num_pages<=5:
        #特例1：如果不够5页则直接返回数据页码数字
        plist=paginator.page_range
    else:
        #如果总页面大于5则进行公式去处
        if pindex<=2:
            #特例2：如果是第1、2则固定为1,2,3,4,5
            plist=range(1,6)
        elif pindex>=paginator.num_pages-1:
            #特例2：如果是末1、末2，已知总页数为n则固定为n-4,n-3,n-2,n-1,n
            plist=range(paginator.num_pages-4,paginator.num_pages+1)
        else:
            #没有特例，公式计算
            plist=range(pindex-2,pindex+3)

    context={'title':'商品列表','isCart':1,
             't':t,'new':new,'page':page,
             'order':order,'plilst':plist}
    return render(request,'tt_goods/list.html',context)
'''
当前是第8页，则显示为 6 7 8 9 10
当前是第5页，则显示为 3 4 5 6 7
[page.number-2,page.number+2]
plist=range(page.number-2,page.number+3)
特例2：如果是第1、2、末1、末2有问题
特例1：如果不够5页则全显示
'''

def detail(request,gid):
    #根据编号查询商品
    goods=GoodsInfo.objects.filter(id=gid)
    #判断编号是否合法
    if goods:
        goods1=goods[0]
        #更新点击量
        goods1.gclick+=1
        goods1.save()
        #当前商品对应分类
        gtype=goods1.gtype
        #获取这个分类的最新的2个商品
        new=gtype.goodsinfo_set.all().order_by('-id')[0:2]

        context={'title':'商品详情','isCart':1,'goods':goods1,'new':new}
        response=render(request, 'tt_goods/detail.html', context)
        # 记录最近浏览
        '''
        先读取原来写好的商品编号，在这个基础上添加上最新的
        最多存储5个最近浏览，所以结构为列表[]
        注意：cookie中只能存字符串，所以需要将列表与字符串相互转换,
        ""90,30,30,60""
        '''
        #读取浏览器中已经浏览过的商品编号
        zjll_str=request.COOKIES.get('zjll','')
        #cookie中只能存字符串，先转换成列表再进行添加
        zjll_list=zjll_str.split(',')
        #如果当前编号已经存在则删除
        if gid in zjll_list:
            zjll_list.remove(gid)
        #将当前编号加入第一个
        zjll_list.insert(0,gid)
        #如果当前个数超过5个则删除最后一个
        if len(zjll_list)>5:
            zjll_list.pop()
        #将列表转换成字符串，用于存入cookie
        zjll_str=','.join(zjll_list)
        #存入cookie
        response.set_cookie('zjll',zjll_str)

        return response
    else:
        return render(request,'404.html')

from haystack.generic_views import SearchView
'''
如果当前地址是search/?a=2
href="?q=1"
==>seach/?q=1
http://127.0.0.1:8000/search/?q=%E5%A5%87%E5%BC%82%E6%9E%9C&page=1
'''
class MySearchView(SearchView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')
        # return queryset.order_by('-gclick')
        # return queryset.order_by('gprice')
    # ordering = '-gclick'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['isLeft']=2
        context['isCart']=1
        return context
