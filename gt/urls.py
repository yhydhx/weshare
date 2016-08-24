from django.conf.urls import patterns, include, url

from django.contrib import admin
from frontEnd.views import *
from backEnd.views import *

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('frontEnd.urls')),
                       url(r'^dc/', include('backEnd.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^alipay/', include('payment.urls')),
                       url(r'^bill/', include('bill.urls')),
                       (r'^files/(?P<path>.*)','django.views.static.serve',{'document_root':settings.UPLOAD_PATH}), 
                       )
