from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from . import task
from . import user_decorators
from tt_goods.models import GoodsInfo
from tt_order.models import OrderInfo,OrderDetailInfo
from django.core.paginator import Paginator,Page
# Create your views here.

def register(request):
    context={'title':'注册','isTop':2}
    return render(request,'tt_user/register.html',context)
def register_handle(request):
    #接收数据
    dict=request.POST
    uname=dict.get('user_name')
    pwd=dict.get('pwd')
    email=dict.get('email')
    #加密
    s1=sha1()
    s1.update(pwd.encode('utf-8'))
    pwd_sha1=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=pwd_sha1
    user.email=email
    user.save()
    #发送邮件，通知celery去执行这个任务
    task.sendmail.delay(user)
    #提示激活
    return HttpResponse('请到邮箱激活，然后再登录')
def register_uname(request):
    #接收请求的用户名
    uname=request.GET.get('uname')
    #判断是否存在
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})
def active(request):
    #设置结果默认值
    ok=0
    url='/user/register/'
    uid=request.GET.get('uid')
    #根据编号查询用户
    user=UserInfo.objects.filter(id=uid)
    #如果用户存在则修改激活状态
    if user:
        #设置激活
        user[0].isActive=True
        user[0].save()
        #设置结果
        ok=1
        url='/user/login/'
    return render(request,'tt_user/active.html',{'ok':ok,'url':url})

def login(request):
    #获取用户名
    uname=request.COOKIES.get('uname','')

    context={'title':'登录','uname':uname,'isTop':2}
    return render(request,'tt_user/login.html',context)
def login_handle(request):
    #接收用户名、密码
    dict=request.POST
    uname=dict.get('username')
    upwd=dict.get('pwd')
    rem=int(dict.get('rem','0'))
    #构造响应报文
    context = {'title': '登录处理', 'uname': uname, 'upwd': upwd,
               'error_name': 0,'error_pwd':0,'isTop':2}
    #根据用户名查询数据
    users=UserInfo.objects.filter(uname=uname,isActive=True,isDelete=False)
    #如果查询到数据，则用户名正确
    if users:
        #获取当前用户
        user=users[0]
        #对密码进行sha1加密
        s1=sha1()
        s1.update(upwd.encode('utf-8'))
        upwd_sha1=s1.hexdigest()

        #判断密码是否正确
        if upwd_sha1==user.upwd:

            #记录当前登录的用户
            request.session['uid']=user.id
            request.session['uname']=uname

            #如果密码正确，则转到原页面，如果没有记录则转到首页
            url=request.session.get('url','/')
            response= redirect(url)
            #记住用户名
            if rem==1:
                #记住
                response.set_cookie('uname',uname,expires=60*60*24*7)
            else:
                #如果之前记住过，则清除
                response.set_cookie('uname','',expires=-1)

            return response
        else:
            #如果密码错误则提示
            context['error_pwd']=1
            return render(request, 'tt_user/login.html', context)
    else:
        #如果未查到数据，则说明用户名错误
        context['error_name']=1
        return render(request,'tt_user/login.html',context)

def logout(request):
    #登录时将用户状态保存在session中，退出将所有的session删除即可
    request.session.flush()
    return redirect('/user/login/')

@user_decorators.islogin
def info(request):
    #在登录时将用户编号存入session，在这里可以获取
    uid=request.session.get('uid')
    #根据用户编号查询用户对象
    user=UserInfo.objects.get(id=uid)
    #查询最近浏览
    zjll_str=request.COOKIES.get('zjll')
    glist = []
    if zjll_str:
        zjll_list=zjll_str.split(',')#[1,2,3,]
        if '' in zjll_list:
            zjll_list.remove('')
        for gid in zjll_list:
            glist.append(GoodsInfo.objects.get(id=gid))

    context={'title':'用户中心','user':user,'glist':glist}
    return render(request,'tt_user/info.html',context)
@user_decorators.islogin
def site(request):
    #获取当前用户
    uid=request.session.get('uid')
    #查询当前用户的所有收货地址
    addrlist=AddressInfo.objects.filter(user_id=uid)

    context={'title':'收货地址','addrlist':addrlist}
    return render(request,'tt_user/site.html',context)
@user_decorators.islogin
def site_add(request):
    #接收请求
    dict=request.POST
    sjr=dict.get('sjr')
    sjh=dict.get('sjh')
    sheng=dict.get('sheng')
    shi=dict.get('shi')
    qx=dict.get('qx')
    addr=dict.get('addr')
    #创建address对象
    address=AddressInfo()
    address.sjr=sjr
    address.sjh=sjh
    address.user_id=request.session.get('uid')
    address.sheng=sheng
    address.shi=shi
    address.qu=qx
    address.addr='%s %s %s %s'%(getnamebyid(sheng),getnamebyid(shi),getnamebyid(qx),addr)
    address.save()
    #回到收货地址列表页面
    return redirect('/user/site/')
def sheng(request):
    #接收请求的编号
    sid=request.GET.get('sid','0')
    if sid=='0':
        #查询所有的省信息
        sheng=AreaInfo.objects.filter(aParent__isnull=True)
    else:
        #如果sid是省编号则查询对应的市，如果sid是市编号则查询对应的区县
        sheng=AreaInfo.objects.filter(aParent_id=sid)
    #将省对象转换成json对象，再将所有json对象加入列表中
    slist=[]
    for s in sheng:
        #{id:***,title:***}
        slist.append({'id':s.id,'title':s.atitle})
    #[{id:,title:},{},{}....]
    return JsonResponse({'sheng':slist})
#根据地区编号查询地区的名称
def getnamebyid(sid):
    return AreaInfo.objects.get(id=sid).atitle
'''

'''
#查询当前用户的订单
@user_decorators.islogin
def order(request):
    uid=request.session.get('uid')
    #查询当前用户的订单数据
    order_list=OrderInfo.objects.filter(user_id=uid).order_by('-odate')
    #分页
    pindex=int(request.GET.get('page','1'))
    paginator=Paginator(order_list,1)
    page=paginator.page(pindex)

    context={'title':'我的订单','page':page}
    return render(request,'tt_user/order.html',context)
