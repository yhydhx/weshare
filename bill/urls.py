from django.conf.urls import patterns, url

from bill import views

urlpatterns = patterns('',
                       url(r'^(?P<method>\w+)/?(?P<Oid>\w*)$', views.bill,name ='bill'), 
                       )
