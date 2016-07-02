# Create your views here.
# coding: utf-8  
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
#from blog.models import Poll,Choice,Blog
from django import forms
from gt.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib


def index(request):
	
	return render(request,"frontEnd/index.html")

def __checkin__(request):


    try:
        request.session['username']
    except KeyError,e:
    	print "KeyError"
    	return HttpResponseRedirect('login.html')

def login(request):
    return render(request, 'blog/login.html' )

def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")

