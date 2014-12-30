# coding=utf-8

from wxstore.models import Store, Order, Address
from wxstore.format import TEXT_IMG_ITEM
from string import atoi
from urllib import urlencode

import sys
reload(sys)
sys.setdefaultencoding('utf8')

URL_PREFIX = "http://anyhelp.sinaapp.com/static/"

# These are interactions in weixin
def getMenu(wxaccount, params):
    allStores = Store.objects.all().order_by('-rank')
    num = allStores.count()
    self_head = TEXT_IMG_ITEM % ("店小二微信订餐，盐工新区第一微信综合服务平台!", "点击此查看更多商家！", "http://anyhelp-image.stor.sinaapp.com/head1_360X200.jpg", "%s%s%s" % (URL_PREFIX + "store.html", "?focus=yes&user=", wxaccount))
    self_intr = TEXT_IMG_ITEM % ("点击此处查看更多商家", "点击此查看更多商家！", "http://anyhelp-image.stor.sinaapp.com/logo.jpg", "%s%s%s" % (URL_PREFIX + "store.html", "?focus=yes&user=", wxaccount))
    if num == 0:
        return [2, "%s%s" % (TEXT_IMG_ITEM % ("当前还没有商家", "火热招租中，您的关注是我们最大的动力！招商电话：18810001796,联系人:张先生", "http://www.baidu.com/img/bdlogo.gif", "#"), self_intr)]
    if num >= 7:
        allStores = allStores[:7]
        num = 7
    ret = []
    ret.append(self_head)
    for store in allStores:
        params = {'user': wxaccount, 'sid': store.pk, 'name': store.name};
        url = "%s?%s" % (store.url if store.url else (URL_PREFIX+'good.html'), urlencode(params))
        ret.append(TEXT_IMG_ITEM % ('%s:%s' % (store.name, store.description), "", store.img, url))
    ret = "".join(ret)
    ret += self_intr
    return [num + 2, ret]

def getOrder(wxaccount, params):
    myOrder = Order.objects.filter(user=wxaccount, status__lt=Order.FINISHED).order_by('-pub_date')
    if myOrder.count() == 0:
        return [params[0]]
    i = 1
    ret = params[1]
    for order in myOrder:
        ret += "%s.订单-%s\n" % (str(i), order.num)
        i = i + 1
    return [ret + params[2]]

def getAddr(wxaccount, params):
    myAddresses = Address.objects.filter(user=wxaccount)
    if myAddresses.count() == 0:
        return [params[0]]
    ret = params[1]
    i = 1
    for address in myAddresses:
        ret += "%s.%s\n" % (str(i), address.alias)
        i = i + 1
    return [ret + params[2]]

# These always return a string as the result
def watchAddr(wxaccount, params, args):
    if len(args) != 1:
        return params[0]
    addresses = Address.objects.filter(user=wxaccount, alias=args[0])
    if addresses.count() <= 0:
        return params[1]
    address = addresses[0]
    return "%s:\n%s\n%s\n%s\n%s" % (address.alias, address.name, address.street, address.detail, address.phone)

def rmAddr(wxaccount, params, args):
    if len(args) != 1:
        return params[0]
    addresses = Address.objects.filter(user=wxaccount, alias=args[0])
    if addresses.count() <= 0:
        return params[1]
    ret = "%s%s" % (params[2], addresses[0].alias)
    addresses[0].delete()
    return ret

def renameAddr(wxaccount, params, args):
    if len(args) != 2:
        return params[0]
    addresses = Address.objects.filter(user=wxaccount, alias=args[0])
    if addresses.count() <= 0:
        return params[1]
    if len(args[1]) > 7:
        return params[2]
    address = addresses[0]
    address.alias = args[1]
    address.save()
    return "%s:%s -> %s。" % (params[3], args[0], args[1])

def watchOrder(wxaccount, params, args):
    if len(args) != 1:
        return params[0]
    orderRes = Order.objects.filter(user=wxaccount, finished=False).order_by('-pub_date')
    args[0] = atoi(args[0])
    if orderRes.count() < args[0]:
        return params[1]
    buySet = orderRes[args[0]-1].buy_set.all()
    ret = ["%s X %s" % (buy.good.name, buy.num) for buy in buySet]
    return "%s:\n%s" % (params[2], "\n".join(ret))

def urgeOrder(wxaccount, params, args):
    if not 0 < len(args) <= 2:
        return params[0]
    orderRes = Order.objects.filter(user=wxaccount, finished=False).order_by('-pub_date')
    args[0] = atoi(args[0])
    if orderRes.count() < args[0]:
        return params[1]
    # send message to deliveryman
    # say = args[1] or params[2]
    # sendMessageToDeliveryman("%s:%s,%s:%s" % (params[3], orderRes[args[0].id], params[4], say)
    return params[2]

def cancleOrder(wxaccount, params, args):
    if len(args) != 1:
        return params[0]
    myOrder = Order.objects.filter(user=wxaccount, finished=False).order_by('-pub_date')
    args[0] = atoi(args[0])
    if myOrder.count() < args[0]:
        return params[1]
    order = myOrder[args[0]-1]
    ret = "%s：%s" % (params[2], order.num)
    order.delete()
    return ret

def registSeller(wxaccount, params, args):
    if len(args) != 2:
        return params[0]
    stores = Store.objects.filter(phone=args[0], password=args[1])
    if stores.count() == 0:
        return params[1]
    existStores = Store.objects.filter(owner=wxaccount)
    if existStores.count() > 0:
        return params[2]
    s = stores[0]
    s.owner = wxaccount
    s.save()
    return params[3]
