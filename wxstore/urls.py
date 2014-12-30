from django.conf.urls import patterns, url

from wxstore import views, pages, seller

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^service', views.handle, name='service'),
    url(r'^stores', pages.getStore, name='stores'),
    url(r'^goods', pages.getGoods, name='goods'),
    url(r'^addresses', pages.getAddresses, name='addresses'),
    url(r'^addOrder', pages.addOrder, name='addOrder'),
    url(r'^myOrder', pages.myOrder, name='myOrder'),
    url(r'^delOrder', pages.delOrder, name='delOrder'),
    url(r'^login', seller.login, name='login'),
    url(r'^hasLogin', seller.hasLogin, name='hasLogin'),
    url(r'^regist', seller.regist, name='regist'),
    url(r'^handleOrder', seller.handleOrder, name='handleOrder'),
    url(r'^sendOrder', seller.sendOrder, name='sendOrder'),
    url(r'^finishOrder', seller.finishOrder, name='finishOrder'),
    url(r'^getUnfinishedOrder', seller.getUnfinishedOrder, name='getUnfinishedOrder'),
    url(r'^getFinishedOrder', seller.getFinishedOrder, name='getFinishedOrder'),
    url(r'^myGoods', seller.myGoods, name='myGoods'),
    url(r'^addGoods', seller.addGoods, name='addGoods'),
    url(r'^delGoods', seller.delGoods, name='delGoods'),
    url(r'^updateGoods', seller.updateGoods, name='updateGoods'),
)
