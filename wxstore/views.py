# Create your views here.
# coding=utf-8

from django.http import HttpResponse
import hashlib, time, memcache
from xml.etree import ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from wxstore.format import TEXT
from wxstore.route import REPLY, COMMAND

TOKEN = 'weixin'
MC = memcache.Client(['127.0.0.1:12000'])

def index(request):
    return HttpResponse("Hello World!")

@csrf_exempt
def handle(request):
    params = request.GET
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)

    args = [TOKEN, timestamp, nonce]
    args.sort()
    tmpstr="%s%s%s" % tuple(args)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    #if tmpstr != signature:
    #    return HttpResponse('Auth failed!')

    if params.has_key('echostr'):
        return HttpResponse(echostr)

    if request.body:
        xml = ET.fromstring(request.body)
        me = xml.find("ToUserName").text
        user = xml.find("FromUserName").text
        postTime = str(int(time.time()))
        msgType = xml.find("MsgType").text
        if msgType == 'event':
            e = xml.find('Event').text
            if e == 'subscribe':
                return HttpResponse(TEXT % (user, me, postTime, '欢迎光临，非常高兴能为您服务！回复h开始尽享方便快捷生活吧~'))
            elif e == 'unsubscribe':
                return HttpResponse(TEXT % (user, me, postTime, '非常荣幸能为您服务！下次再见～'))
        # msgid check. if repeat, reponse with ""
        msgid = xml.find("MsgId").text
        if not MC.get(msgid):
            # cache msgid for 1 min with MC(memcache client)
            MC.add(msgid, '1', 60)
            content = xml.find("Content").text
            if content.strip() in REPLY:
                fmt, result = REPLY[content]
                if isinstance(result, basestring):
                    return HttpResponse(fmt % (user, me, postTime, result))
                else:
                    op, params = result
                    return HttpResponse(fmt % tuple([user, me, postTime] + op(user, params)))
            else:
                # a little like command mode, and they are all use TEXT format
                args = content.split()
                if args[0] in COMMAND:
                    op, params = COMMAND[args[0]]
                    return HttpResponse(TEXT % (user, me, postTime, op(user, params, args[1:])))
                # command can not be parsed
                return HttpResponse(TEXT % (user, me, postTime, "回复m查看所有商家，谢谢您的关注与支持。"))

        # msg has been handle, response nothing
        return HttpResponse(TEXT % (user, me, postTime, ""))

    return HttpResponse("Any help I can provide you? %s" % (request.get_full_path()))

