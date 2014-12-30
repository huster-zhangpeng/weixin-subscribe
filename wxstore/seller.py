# coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect
from wxstore.models import Store, Order, Good
from django.views.decorators.csrf import csrf_exempt
from string import atoi
from datetime import *
import json  #, hashlib

@csrf_exempt
def hasLogin(request):
    if request.session.has_key('seller') and request.session['seller'] != "":
        return HttpResponse(json.dumps({'ret':0, 'msg':'ok'}))
    return HttpResponse(json.dumps({'ret':1, 'msg':"您还没有登录！"}))

@csrf_exempt
def login(request):
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    # password = hashlib.md5(password).hexdigest().upper();
    stores = Store.objects.filter(phone=phone, password=password)
    if stores.count() != 0:
        if stores[0].owner == "":
            return HttpResponse(json.dumps({'ret':2, 'msg':"您还未绑定微信！"}))
        request.session['seller'] = stores[0].owner
        request.session['sid'] = stores[0].pk
        return HttpResponse(json.dumps({'ret':0, 'msg': 'ok'}))
    return HttpResponse(json.dumps({'ret': 1, 'msg': "用户名不存在或密码错误！"}))

@csrf_exempt
def addGoods(request):
    if not request.session.has_key('sid') or request.session['sid'] == "":
        return HttpResponseRedirect("../static/login.html")
    sid = request.session['sid']
    store = Store.objects.get(pk=sid)
    gname = request.POST.get('gname', None)
    gprice = request.POST.get('gprice', None)
    gremain = request.POST.get('gremain', "-1")
    gdesc = request.POST.get('gdesc', None)
    gimg = request.POST.get('gimg', None)
    grank = request.POST.get('grank', '0')
    goods = Good(name=gname, price=float(gprice), remain=atoi(gremain), description=gdesc, img=gimg, rank=atoi(grank))
    store.good_set.add(goods)
    store.save()
    return HttpResponseRedirect("../static/mgoods.html")

@csrf_exempt
def myGoods(request):
    if not request.session.has_key('sid') or request.session['sid'] == "":
        return HttpResponseRedirect("../static/login.html")
    sid = request.session['sid']
    store = Store.objects.get(pk=sid)
    ret = [{'gname': goods.name, 'gprice': goods.price, 'gremain': goods.remain, 'gdesc': goods.description,
            'gid': goods.pk, 'grank': goods.rank, 'gimg': goods.img} for goods in store.good_set.all()]
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))


@csrf_exempt
def updateGoods(request):
    if not request.session.has_key('sid') or request.session['sid'] == "":
        return HttpResponse(json.dumps({'ret':1, 'msg':"您的身份已过期，请重新登录！"}))
    gid = request.POST.get('gid', None)
    goods = Good.objects.get(pk=atoi(gid))
    goods.name = request.POST.get('gname', None)
    goods.price = float(request.POST.get('gprice', None))
    goods.remain = atoi(request.POST.get('gremain', "-1"))
    goods.description = request.POST.get('gdesc', None)
    goods.img = request.POST.get('gimg', None)
    goods.rank = atoi(request.POST.get('grank', '0'))
    goods.save()
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok'}))

@csrf_exempt
def delGoods(request):
    if not request.session.has_key('sid') or request.session['sid'] == "":
        return HttpResponse(json.dumps({'ret':1, 'msg':"您的身份已过期，请重新登录！"}))
    gid = request.POST.get('gid', None)
    goods = Good.objects.get(pk=atoi(gid))
    goods.delete()
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok'}))

@csrf_exempt
def regist(request):
    phone = request.POST.get('phone', None)
    password = request.POST.get('password', None)
    sname = request.POST.get('sname', None)
    sdesc = request.POST.get('sdesc', None)
    simg = request.POST.get('simg', None)
    saddr = request.POST.get('saddr', None)

    stores = Store.objects.filter(phone=phone)
    if stores.count() > 0:
        return HttpResponse(json.dumps({'ret':1, 'msg':"此手机号已被使用！"}))

    # password = hashlib.md5(password).hexdigest().upper();
    s = Store(phone=phone, password=password, name=sname, description=sdesc, img=simg, addr=saddr)
    s.save()

    return HttpResponse(json.dumps({'ret':0, 'msg': 'ok'}))

@csrf_exempt
def handleOrder(request):
    oid = request.POST.get('oid', None)
    try:
        o = Order.objects.get(pk=oid)
        if o.status >= Order.FINISHED:
            return HttpResponse(json.dumps({'ret':1, 'msg': '此订单已被取消或已完成！'}))
        if o.status == Order.NEW:
            o.status = Order.HANDLING
            o.save();
        return HttpResponse(json.dumps({'ret':0, 'msg': 'ok'}))
    except Order.DoesNotExist:
        return HttpResponse(json.dumps({'ret':2, 'msg':"此订单已被取消！"}))

@csrf_exempt
def sendOrder(request):
    oid = request.POST.get('oid', None)
    try:
        o = Order.objects.get(pk=oid)
        if o.status >= Order.FINISHED:
            return HttpResponse(json.dumps({'ret':1, 'msg': '此订单已完成！'}))
        if o.status == Order.HANDLING:
            o.status = Order.SENDING
            o.save();
        return HttpResponse(json.dumps({'ret':0, 'msg': 'ok'}))
    except Order.DoesNotExist:
        return HttpResponse(json.dumps({'ret':2, 'msg':"此订单已被取消！"}))

@csrf_exempt
def finishOrder(request):
    oid = request.POST.get('oid', None)
    try:
        o = Order.objects.get(pk=oid)
        if o.status >= Order.FINISHED:
            return HttpResponse(json.dumps({'ret':1, 'msg': '此订单已完成！'}))
        if o.status == Order.SENDING:
            o.status = Order.FINISHED
            o.save();
        return HttpResponse(json.dumps({'ret':0, 'msg': 'ok'}))
    except Order.DoesNotExist:
        return HttpResponse(json.dumps({'ret':2, 'msg':"此订单已被取消！"}))

@csrf_exempt
def getUnfinishedOrder(request):
    #seller = None
    #if 'seller' in request.session:
    #    seller = request.session['wxid']
    #else:
    #    return HttpResponse(json.dumps({'ret':1, 'msg':"您还未登录！"}))
    seller = request.session['seller']

    stores = Store.objects.filter(owner=seller)
    if stores.count() == 0:
        return HttpResponse(json.dumps({'ret':2, 'msg':"错误！您可能还没在微信中注册！"}))

    store = stores[0]
    myOrder = store.order_set.all().filter(status__lt=Order.FINISHED).order_by('-pub_date')
    ret = [{'id': o.pk, 'o_no': o.num, 'store': o.store.name, 'cost': o.cost, 'rt': o.request_time,
            'buy':[{'name': buy.name, 'price': buy.price, 'num': buy.num} for buy in o.buy_set.all()],
            'addr':{'name': o.name, 'street': o.street, 'detail': o.detail, 'phone': o.phone},
            'remarks': o.remarks, 'pub_date': str(o.pub_date), 'status': o.status} for o in myOrder]
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))

@csrf_exempt
def getFinishedOrder(request):
    #seller = None
    #if 'seller' in request.session:
    #    seller = request.session['wxid']
    #else:
    #    return HttpResponse(json.dumps({'ret':1, 'msg':"您还未登录！"}))
    seller = request.session['seller']

    stores = Store.objects.filter(owner=seller)
    if stores.count() == 0:
        return HttpResponse(json.dumps({'ret':2, 'msg':"错误！您可能还没在微信中注册！"}))

    store = stores[0]
    today = date.today()
    week = today.isoweekday() % 7;
    start = datetime(today.year, today.month, 1)
    if today.day <= week:
        start = today - timedelta(days=week)
    myOrder = store.order_set.all().filter(status=Order.FINISHED, pub_date__gt=start).order_by('-pub_date')
    ret = [{'id': o.pk, 'o_no': o.num, 'store': o.store.name, 'cost': o.cost, 'rt': o.request_time,
            'buy':[{'name': buy.name, 'price': buy.price, 'num': buy.num} for buy in o.buy_set.all()],
            'addr':{'name': o.name, 'street': o.street, 'detail': o.detail, 'phone': o.phone},
            'remarks': o.remarks, 'pub_date': str(o.pub_date), 'status': o.status} for o in myOrder]
    return HttpResponse(json.dumps({'ret':0, 'msg':'ok', 'data':ret}))


