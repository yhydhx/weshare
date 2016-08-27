from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^test/$', views.test, name='test'),
                       url(r'^school/(?P<method>\w+)/?(?P<Oid>\w*)$', views.school,name ='school'),
                       url(r'^register_host/(?P<method>\w+)/?(?P<Oid>\w*)$', views.register_host,name ='register_host'),
                       url(r'^user/(?P<method>\w+)/?(?P<Oid>\w*)$', views.user,name ='user'),
                       url(r'^bill/(?P<method>\w+)/?(?P<Oid>\w*)$', views.bill,name ='bill'),
						url(r'^general_search/$', views.general_search, name='general_search'),

                       
                       )
