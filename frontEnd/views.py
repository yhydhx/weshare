# Create your views here.
# coding: utf-8  
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
# from blog.models import Poll,Choice,Blog
from django import forms
from gt.models import *
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib


def index(request):
    if request.user.is_authenticated():
        return render_to_response('frontEnd/index.html', {'user': request.user})
    else:
        return render_to_response('frontEnd/index.html')


@csrf_exempt
def init_register(request):  # 暂时统一用用户名注册,以后的一些坑以后再填
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password'] and request.POST['password-confirm']:
            if request.POST['password'] == request.POST['password-confirm']:  # 初级的用户注册完成了
                username = request.POST['username']
                password = request.POST['password']
                if 0:  # 这里的查重等会再弄
                    return HttpResponse('用户名已经存在请换一个')
                else:
                    base_user = User(username=username,
                                     password=password,
                                     email='',
                                     first_name='',
                                     last_name='', )
                    base_user.save()
                    init_user = Host(base_user=base_user)
                    init_user.save()
                    return render_to_response('frontEnd/login.html', context_instance=RequestContext(request))
            else:
                return HttpResponse('请输入两次相同的密码')
        else:
            return HttpResponse('清完成这个表单')
    else:
        return render_to_response('frontEnd/account.html')


def __checkin__(request):
    try:
        request.session['username']
    except KeyError, e:
        print "KeyError"
        return HttpResponseRedirect('login.html')


def login(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return HttpResponse('用户名或者密码不正确,或者账户处于被冻结的状态')
        else:
            return HttpResponse('请填入用户名和密码')
    else:
        return render_to_response('frontEnd/index.html', context_instance=RequestContext(request))


def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")


def database(request):
    user = User(username='xxx', password='xxx')
    user.save()
    return HttpResponse('ddfdfd')
