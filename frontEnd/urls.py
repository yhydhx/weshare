from django.conf.urls import patterns, url

from frontEnd import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^database$', views.database, name='index'),
)