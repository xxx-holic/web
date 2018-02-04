from django.shortcuts import render
from django.db import transaction
from tt_user.user_decorators import islogin
from tt_user.models import AddressInfo
from tt_cart.models import CartInfo
from .models import OrderInfo,OrderDetailInfo
from datetime import datetime
from django.http import JsonResponse
# Create your views here.
@islogin
def index(request):
    #查询当前用户的收货地址
    uid=request.session.get('uid')
    addr_list=AddressInfo.objects.filter(user_id=uid)
    #查询选中的购物车数据
    cids=request.GET.getlist('cid')
    cart_list=CartInfo.objects.filter(id__in=cids)

    context={'title':'确认订单','addr_list':addr_list,'cart_list':cart_list}
    return render(request,'tt_order/index.html',context)


@transaction.atomic
@islogin
def handle(request):
    uid=request.session.get('uid')
    #接收数据：地址、购物车编号
    dict=request.POST
    addr=dict.get('addr')
    cids=dict.getlist('cid')
    #设置事务的保存点，之后的数据操作都在事务中
    sid=transaction.savepoint()
    #1.创建订单
    order=OrderInfo()
    order.oid='%s%06d'%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
    order.user_id=uid
    order.ototal=0
    order.oaddress=addr
    order.save()

    #2.查询提交的购物车数据
    carts=CartInfo.objects.filter(id__in=cids)
    total=0
    isOk=True
    for cart in carts:
        #3.逐个判断库存是否足够
        if cart.nums<=cart.goods.gkucun:
            # 4.如果足够则继续操作
            price=cart.goods.gprice
            # 4.1创建详单
            detail=OrderDetailInfo()
            detail.order=order
            # detail.order_id=order.oid
            detail.goods=cart.goods
            detail.price=price
            detail.count=cart.nums
            detail.save()
            # 4.2减少库存
            cart.goods.gkucun-=cart.nums
            cart.goods.save()
            # 4.3计算总价
            total+=price*cart.nums
            # 4.4 删除购物车数据
            cart.delete()
        else:
            # 5.如果不够则回到购物车
            isOk=False
            break
    #判断整个操作是否成功
    if isOk:
        #存储总价
        order.ototal=total
        order.save()
        #提交
        transaction.savepoint_commit(sid)
    else:
        #回滚
        transaction.savepoint_rollback(sid)

    return JsonResponse({'ok':isOk})
