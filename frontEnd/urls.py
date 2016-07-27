from django.conf.urls import patterns, url

from frontEnd import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^account/$', views.init_register, name='index'),
                       # url(r'^database$', views.database, name='index'),
                       url('^logout/$', views.logout, name='index'),
                       url(r'^login/$', views.login, name='index'),
                       url(r'^iforget/$', views.i_forget, name='forget'),
                       url(r'^iforget/(.*)/$', views.i_forget),
                       url(r'^complete-account/$', views.complete_account, name='index'),
                       url(r'^host-center/$', views.host_center, name='host'),
                       url(r'^modify-account/$', views.modify_account, name='modify'),
                       url(r'^image-receive/$', views.image_receive),
                       url(r'^complete-account-feature/', views.complete_account_feature, name='cp'),

                       url('^image-library/', views.image_library, name='image-library'),
                       # url('^feature_ajax/', views.feature_ajax, name='feature_ajax'),
                       url(r'^about$', views.about, name='about'),
                       url(r'^service$', views.service, name='service'),
                       url(r'^school/(?P<method>\w+)/?(?P<Oid>\w*)$', views.school,name ='school'),
                       url(r'^user/(?P<method>\w+)/?(?P<Oid>\w*)$', views.user,name ='user'),   
                       )
