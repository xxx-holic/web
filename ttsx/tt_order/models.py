from django.db import models

# Create your models here.
#coding=utf-8
from django.db import models
class OrderInfo(models.Model):
    #编号，年月日时分秒（14位）+编号（6位）==》999999
    oid=models.CharField(max_length=20, primary_key=True)
    #用户
    user=models.ForeignKey('tt_user.UserInfo')
    #日期，自动填写为当前时间
    odate=models.DateTimeField(auto_now_add=True)
    #支付状态
    oIsPay=models.BooleanField(default=False)
    #总价，虽然是冗余数据，但是使用频繁，所以单独存下来
    ototal=models.DecimalField(max_digits=6,decimal_places=2)
    #收货地址
    oaddress=models.CharField(max_length=150)

class OrderDetailInfo(models.Model):
    #商品
    goods=models.ForeignKey('tt_goods.GoodsInfo')
    #订单
    order=models.ForeignKey(OrderInfo)
    #单价，快照，商品可能会调价
    price=models.DecimalField(max_digits=5,decimal_places=2)
    #数量
    count=models.IntegerField()
