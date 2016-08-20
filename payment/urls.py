from django.conf.urls import patterns, url

from payment import views

urlpatterns = patterns('',
    url(r'^pay$', views.pay, name='pay'),
    url(r'^notify$', views.alipay_notify_url, name='alipay_notify_url'),
    url(r'^return$', views.alipay_return_url, name='alipay_return_url'),
    url(r'^verify/(?P<cbid>\w+)$', views.verify, name='verify'),


    #url(r'index',views.news, name="news"),
    #url(r'^contact$', views.contact,name ='contact'),
)
