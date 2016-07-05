from django.conf.urls import patterns, url

from backEnd import views

urlpatterns = patterns('',
    url(r'^login\.html$', views.login, name='login'),
    #url(r'index',views.news, name="news"),
    #url(r'^contact$', views.contact,name ='contact'),
    url(r'^addUser$', views.addUser,name ='addUser'),
    url(r'^loginCertifacate$', views.loginCertifacate,name ='loginCertifacate'),
    url(r'^addUserView$', views.addUserView,name ='addUserView'),
    url(r'^changePasswd$', views.changePasswd,name ='changePasswd'),
    url(r'^logout$', views.logout,name ='logout'),
 
    url(r'^province/(?P<method>\w+)/?(?P<Oid>\w*)$', views.province,name ='province'),
    url(r'^school/(?P<method>\w+)/?(?P<Oid>\w*)$', views.school,name ='school'),
    url(r'^topic/(?P<method>\w+)/?(?P<Oid>\w*)$', views.topic,name ='topic'),
    url(r'^user/(?P<method>\w+)/?(?P<Oid>\w*)$', views.user,name ='user'),
    url(r'^feature/(?P<method>\w+)/?(?P<Oid>\w*)$', views.feature,name ='feature'),    
    url(r'^test\.html$', views.test, name='test'),
    url(r'^s\.html$', views.s, name='s'),
    '''

    

    #file operation 
    url(r'^addImage$', views.addImage,name ='addImage'),
    url(r'^addImageInfo$', views.addImageInfo,name ='addImageInfo'),
    url(r'^showImgList$', views.showImgList,name ='showImgList'),
    url(r'^deleteImg/(?P<Oid>\w+)$', views.deleteImg,name ='deleteImg'),
    url(r'^test$', views.test,name ='test'),
    '''
)
