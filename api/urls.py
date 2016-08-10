from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^school/(?P<method>\w+)/?(?P<Oid>\w*)$', views.school,name ='school'),
                       url(r'^user/(?P<method>\w+)/?(?P<Oid>\w*)$', views.user,name ='user'),
                       )
