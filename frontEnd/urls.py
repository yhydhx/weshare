from django.conf.urls import patterns, url

from frontEnd import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^account/$', views.init_register, name='index'),
                       # url(r'^database$', views.database, name='index'),
                       url('^logout/$', views.logout, name='index'),
                       url(r'^login/$', views.login, name='index'),
                       url(r'^complete-account/', views.complete_account, name='index'),
                       url(r'^complete-account-icon/', views.complete_account_icon, name='index'),
                       )
