from django.db import models
from tt_goods.models import GoodsInfo
from tt_user.models import UserInfo
# Create your models here.
class CartInfo(models.Model):
    goods=models.ForeignKey(GoodsInfo)
    nums=models.IntegerField()
    user=models.ForeignKey(UserInfo)
