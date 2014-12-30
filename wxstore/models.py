# coding=utf-8

from django.db import models
import time, random

# Create your models here.
class Store(models.Model):
    phone = models.CharField(max_length=20)                 #商家手机，登录用
    password = models.CharField(max_length=64)              #商家访问密码
    owner = models.CharField(max_length=100, blank=True)    #商家的微信号
    # email = models.EmailField()
    name = models.CharField(max_length=50)                  #商家名称
    description = models.CharField(max_length=200)          #商家描述
    img = models.CharField(max_length=700)                  #商家图片
    url = models.CharField(max_length=700, blank=True)      #商家链接地址
    addr = models.CharField(max_length=200)                 #商家地址
    rank = models.PositiveIntegerField(default=0)           #商家竞价显示顺序用，预留着
    pub_date = models.DateField(auto_now_add=True)          #商家创建日期

class Good(models.Model):
    owner = models.ForeignKey(Store)                        #所属商家
    name = models.CharField(max_length=20)                  #名称
    price = models.FloatField()                             #价格
    remain = models.IntegerField(default=-1)                #商品剩余量，-1表示此商品无限
    description = models.CharField(max_length=200)          #描述
    img = models.CharField(max_length=300)                  #图片地址
    rank = models.PositiveIntegerField(default=0)           #显示位置
    avg_rate = models.FloatField(default=0)                 #用户评分
    pub_date = models.DateField(auto_now_add=True)          #商品创建日期

class Rate(models.Model):
    user = models.CharField(max_length=100)                 #用户的微信号
    good = models.ForeignKey(Good)                          #哪个商品
    score = models.PositiveIntegerField()                   #评了多少分
    title = models.CharField(max_length=80)                 #评论标题
    content = models.CharField(max_length=300)              #评论内容
    pub_date = models.DateField(auto_now_add=True)          #评论创建日期

class Address(models.Model):
    alias = models.CharField(max_length=16)                 #地址名，不能超过6个字
    user = models.CharField(max_length=100)                 #用户的微信号
    name = models.CharField(max_length=20)                  #用户的姓名，称呼
    street = models.CharField(max_length=100)               #街、区
    detail = models.CharField(max_length=100)               #楼、单元、层
    phone = models.CharField(max_length=20)                 #手机号码，联系方式

class Order(models.Model):
    NEW = 0
    HANDLING = 1
    SENDING = 2
    FINISHED = 3
    CANCLED = 4
    num = models.CharField(max_length=36)                   #订单号,不简单地用自增主键,为了不让别人看出来我们的订单量
    user = models.CharField(max_length=30)                  #微信帐号，标识用户
    store = models.ForeignKey(Store)                        #所属商家
    request_time = models.CharField(max_length=60)          #要求送达时间
    cost = models.FloatField()                              #总价
    remarks = models.CharField(max_length=200, blank=True)  #用户备注、留言
    status = models.SmallIntegerField(choices=(             #订单状态，4个状态
        (NEW, 'New'),
        (HANDLING, 'Handling'),
        (SENDING, 'Sending'),
        (FINISHED, 'Finished'),
        (CANCLED, 'Cancled')
    ), db_index=True, default=NEW)
    #用户地址的一份copy，为的是用户删除地址后，订单的地址依然有效
    name = models.CharField(max_length=20)                  #用户的姓名，称呼
    street = models.CharField(max_length=100)               #街、区
    detail = models.CharField(max_length=100)               #楼、单元、层
    phone = models.CharField(max_length=20)                 #手机号码，联系方式
    pub_date = models.DateTimeField(auto_now_add=True)      #创建日期

    def save(self):
        while True:
            tmp = "%s%s" % (time.strftime("%Y%m%d"), random.randint(1000,9999))
            repeat = Order.objects.filter(num=tmp)
            if repeat.count() == 0:
                self.num = tmp
                break
        super(Order, self).save()

#订单上的物品
class Buy(models.Model):
    order = models.ForeignKey(Order)                        #所属订单
    gid = models.PositiveIntegerField(db_index=True)        #商品的id，但不是外键
    name = models.CharField(max_length=60)                  #商品名称
    price = models.FloatField()                             #商品价格
    num = models.PositiveIntegerField()                     #数量

