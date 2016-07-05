from django.conf.urls import patterns, include, url

from django.contrib import admin
from frontEnd.views import *
from backEnd.views import *

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('frontEnd.urls')),
                       url(r'^dc/', include('backEnd.urls')),

                       )
