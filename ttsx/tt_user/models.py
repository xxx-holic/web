from django.db import models

# Create your models here.
# 用户
class UserInfo(models.Model):
    # 用户名
    uname = models.CharField(max_length=20)
    # 密码，进行sha1加密
    upwd = models.CharField(max_length=40)  # sha1
    # 邮箱
    email = models.CharField(max_length=30)
    # 激活状态
    isActive = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)


class AreaInfo(models.Model):
    atitle = models.CharField(max_length=20)
    aParent = models.ForeignKey('self', null=True, blank=True)


# 收获地址
class AddressInfo(models.Model):
    # 收件人
    sjr = models.CharField(max_length=20)
    # 收件人手机号
    sjh = models.CharField(max_length=11)
    # 收获地址
    addr = models.CharField(max_length=100)

    isDelete = models.BooleanField(default=False)
    # 外键，与用户关联
    user = models.ForeignKey('UserInfo')
    # 省编号
    sheng = models.IntegerField()
    # 市编号
    shi = models.IntegerField()
    # 区县编号
    qu = models.IntegerField()
