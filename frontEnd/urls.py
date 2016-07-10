from django.conf.urls import patterns, url

from frontEnd import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^account/$', views.init_register, name='index'),
                       # url(r'^database$', views.database, name='index'),
                       url('^logout/$', views.logout, name='index'),
                       url(r'^login/$', views.login, name='index'),
                       url(r'^complete-account/$', views.complete_account, name='index'),
                       url(r'^host-center/$', views.host_center, name='host'),
                       url(r'^modify-account/$', views.modify_account, name='modify'),
                       url(r'^image-receive/$', views.image_receive),
                       url(r'^complete-account-feature/', views.complete_account_feature, name='cp'),
                       url(r'^about$', views.about,name ='about'),
                       url(r'^service$', views.service,name ='service'),
                       url(r'^school$', views.school,name ='school'),
                       )
