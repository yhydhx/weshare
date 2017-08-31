from django.conf.urls import patterns, url

from dota import views

urlpatterns = patterns('',
    url(r'^login\.html$', views.login, name='login'),
    #url(r'index',views.news, name="news"),
    #url(r'^contact$', views.contact,name ='contact'),
    url(r'^addUser$', views.addUser,name ='addUser'),
    url(r'^loginCertifacate$', views.loginCertifacate,name ='loginCertifacate'),
    url(r'^addUserView$', views.addUserView,name ='addUserView'),
    url(r'^changePasswd$', views.changePasswd,name ='changePasswd'),
    url(r'^logout$', views.logout,name ='logout'),
    #url(r'^fake_user$', views.fake_user,name ='fake_user'),
    
    


    url(r'^items/(?P<method>\w+)/?(?P<Oid>\w*)$', views.items,name ='items'), 
    url(r'^province/(?P<method>\w+)/?(?P<Oid>\w*)$', views.province,name ='province'),
    url(r'^school/(?P<method>\w+)/?(?P<Oid>\w*)$', views.school,name ='school'),
    url(r'^topic/(?P<method>\w+)/?(?P<Oid>\w*)$', views.topic,name ='topic'),
    url(r'^minortopic/(?P<method>\w+)/?(?P<Oid>\w*)$', views.minortopic,name ='minortopic'),
    url(r'^user/(?P<method>\w+)/?(?P<Oid>\w*)$', views.user,name ='user'),
    url(r'^feature/(?P<method>\w+)/?(?P<Oid>\w*)$', views.feature,name ='feature'),   
    
    url(r'^menu/(?P<method>\w+)/?(?P<Oid>\w*)$', views.menu,name ='menu'),
    url(r'^doc/(?P<method>\w+)/?(?P<Oid>\w*)$', views.doc,name ='doc'),   

    url(r'^func/(?P<method>\w+)/?(?P<Oid>\w*)$', views.func,name ='func'),   
    url(r'^certification/(?P<method>\w+)/?(?P<Oid>\w*)$', views.certification,name ='certification'),   
    url(r'^appointment/(?P<method>\w+)/?(?P<Oid>\w*)$', views.appointment,name ='appointment'),   

    url(r'^test\.html$', views.test, name='test'),
    url(r'^s\.html$', views.s, name='s'),
    url(r'^email\.html$', views.setEmail, name='setEmail'),
    url(r'^getUserNameList$', views.getUserNameList,name ='getUserNameList'),

    
    '''

    

    #file operation 
    url(r'^addImage$', views.addImage,name ='addImage'),
    url(r'^addImageInfo$', views.addImageInfo,name ='addImageInfo'),
    url(r'^showImgList$', views.showImgList,name ='showImgList'),
    url(r'^deleteImg/(?P<Oid>\w+)$', views.deleteImg,name ='deleteImg'),
    url(r'^test$', views.test,name ='test'),
    '''
)
