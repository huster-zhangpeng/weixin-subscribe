# coding=utf-8

from django.http import HttpResponse
from wxstore.models import Store, Address, Order, Good, Buy
from django.views.decorators.csrf import csrf_exempt
from string import atoi
from django.db import transaction
import json

@csrf_exempt
def delOrder(request):
    oid = request.POST.get('id', None)
    order = Order.objects.get(pk=atoi(oid))
    if order.status > Order.NEW:
        return HttpResponse(json.dumps({'ret':1, 'msg':'订单已经开始处理，不可以删除！'}))
    order.delete()
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok'}))

@csrf_exempt
def getStore(request):
    # user = request.POST.get('user',None)
    stores = Store.objects.all()
    ret = [{'id': store.id, 'name': store.name, 'phone': store.phone, 'url': store.url} for store in stores]
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))

@csrf_exempt
def getGoods(request):
    sid = request.POST.get('sid', None)
    try:
        store = Store.objects.get(pk=sid)
        ret = [{'id':good.pk, 'name': good.name, 'price':good.price} for good in store.good_set.exclude(remain=0).order_by('-pub_date')]
        return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))
    except Store.DoesNotExist:
        return HttpResponse(json.dumps({'ret':-2, 'msg':'not exist'}))
    except:
        return HttpResponse(json.dumps({'ret':-1, 'msg':'error'}))
    pass

@csrf_exempt
def getAddresses(request):
    wxaccount = request.POST.get('user', None)
    addresses = Address.objects.filter(user=wxaccount)
    ret = [{'id': addr.pk, 'alias': addr.alias, 'name': addr.name, 'street': addr.street, 'detail': addr.detail, 'phone': addr.phone} for addr in addresses]
    return HttpResponse(json.dumps({'ret': 0, 'msg': 'ok', 'data': ret}))

@csrf_exempt
@transaction.commit_manually
def addOrder(request):
    wxaccount = request.POST.get('user', None)
    sid = request.POST.get('sid', None)
    cart = json.loads(request.POST.get('cart', None))
    c = request.POST.get('cost', None)
    a = json.loads(request.POST.get('addr', None))
    rt = request.POST.get('requestTime', None)
    r = request.POST.get('tag', None)

    addr = None
    if a['type'] == 'new':
        i = 0
        while True:
            tmp = Address.objects.filter(user=wxaccount, alias="%s%s" % ("常用地址", i))
            if tmp.count() == 0:
                break
            i = i + 1
        addr = Address(user=wxaccount, alias= "%s%s" % ("常用地址", i), name=a['name'], street=a['street'], detail=a['detail'], phone=a['phone'])
        addr.save()
    else:
        addr = Address.objects.get(pk=a['aid'])

    s = Store.objects.get(pk=sid)
    o = Order(user=wxaccount, store=s, request_time=rt, cost=c, remarks=r, name=addr.name, street=addr.street, detail=addr.detail, phone=addr.phone)
    o.save()
    for gid in cart:
        try:
            good = Good.objects.get(pk=gid)
            if good.remain == 0:
                transaction.rollback()
                return HttpResponse(json.dumps({'ret':2, 'msg': '某商品已卖完！'}))
            if good.remain > 0:
                good.remain = good.remain - 1
                good.save()
            b = Buy(gid=atoi(gid), num=cart[gid]['num'], name=cart[gid]['name'], price=float(cart[gid]['price'][1:]))
            o.buy_set.add(b)
        except Good.DoesNotExist:
            transaction.rollback()
            return HttpResponse(json.dumps({'ret':1, 'msg': '某商品不存在！'}))

    o.save()
    transaction.commit()
    return HttpResponse(json.dumps({'ret': 0, 'msg': 'ok'}))

@csrf_exempt
def myOrder(request):
    wxaccount = request.POST.get('user', None)
    myOrder = Order.objects.filter(user=wxaccount, status__lt=Order.FINISHED).order_by('-pub_date')
    ret = [{'id': o.pk, 'o_no': o.num, 'store': o.store.name, 'cost': o.cost, 'rt': o.request_time,
            'buy':[{'name': buy.name, 'price': buy.price, 'num': buy.num} for buy in o.buy_set.all()],
            'addr':{'name': o.name, 'street': o.street, 'detail': o.detail, 'phone': o.phone},
            'remarks': o.remarks, 'pub_date': str(o.pub_date), 'status': o.status} for o in myOrder]
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))

