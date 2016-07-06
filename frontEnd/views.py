# Create your views here.
# coding: utf-8
from django.forms import forms
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
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib
import chunk
import os


def index(request):
    login_flag = False
    try:
        req_username = request.session['username']
    except KeyError:
        req_username = None
    if req_username:
        user = Host.objects.get(username=req_username)
        login_flag = True
        return render_to_response('frontEnd/index.html', {'current_user': user,
                                                          'login_flag': login_flag})
    else:
        return render_to_response('frontEnd/index.html')


@csrf_exempt
def init_register(request):  # 暂时统一用用户名注册,以后的一些坑以后再填
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password'] and request.POST['password-confirm'] \
                and request.POST['phone'] and request.POST['email']:
            if request.POST['password'] == request.POST['password-confirm']:  # 初级的用户注册完成了
                username = request.POST['username']
                password = request.POST['password']
                phone = request.POST['phone']
                email = request.POST['email']
                try:
                    Host.objects.get(username=username)
                except:
                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                )
                    host.save()
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


@csrf_exempt
def login(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = Host.objects.get(username=username)
                if user.password != password:
                    return HttpResponse('用户名或者密码不正确,或者账户处于被冻结的状态')
                else:
                    request.session['username'] = username
                    return HttpResponseRedirect('/index/')
            except:
                return HttpResponse('用户名或者密码不正确,或者账户处于被冻结的状态')
    else:
        return render_to_response('frontEnd/login.html', {'session_timeout': False},
                                  context_instance=RequestContext(request))


def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")


@csrf_exempt  # 所有有这个东西的全部要删掉到时候重新部署csrf防跨站
def complete_account(request):
    try:
        username = request.session['username']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True},
                                  context_instance=RequestContext(request))
    try:
        host = Host.objects.get(username=username)
    except:
        return HttpResponse('你所持有的session并不在数据库中找到对应内容')
    if request.method == 'POST':
        if request.POST['self-introduction'] and request.POST['gender'] and request.POST['motto'] and \
                request.POST['min-payment'] and request.POST['service-time'] and request.POST['max-payment']:
            self_introduction = request.POST['self-introduction']
            gender = request.POST['gender']
            motto = request.POST['motto']
            min_payment = request.POST['min-payment']
            service_time = request.POST['service-time']
            max_payment = request.POST['max-payment']
            print gender
            if not (gender == u'男' or gender == u'女'):
                return HttpResponse('请填写男或者女')
            if gender == u'男':
                host.gender = 1
            else:
                host.gender = 0
            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment
            host.state = 1
            host.save()
            return HttpResponseRedirect('/index/', context_instance=RequestContext(request))
        else:
            return HttpResponse('请把表单填写完整')
    else:
        return render_to_response('frontEnd/complete-account.html', context_instance=RequestContext(request))


''' class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField() '''


def complete_account_icon(request):  # 注册成为HOST
    try:
        username = request.session['username']
    except:  # 会话失效或者你随意找到了这个url
        return render_to_response('frontEnd/index.html', {'session_timeout': 1},
                                  context_instance=RequestContext(request))
    try:
        host = Host.objects.get(username=username)
    except:
        return HttpResponse('你所持有的session并不能在数据库中找到什么相对应的东西')
    # host已经验证完全。
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        mark_list = hashlib.new('md5', timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S")).hexdigest()
        des_origin_path = settings.UPLOAD_PATH + 'icons/' + mark_list + '.jpeg'  # mark_list是唯一的标志
        try:
            icon = request.FILES['icon']
        except:
            return HttpResponse('你没有携带图片来post我')
        des_origin_file = open(des_origin_path, "wb")
        for chunk in icon.chunks():
            des_origin_file.write(chunk)
        des_origin_file.close()
        host.icon = des_origin_path
        host.save()
        return render_to_response('frontEnd/complete-account.html', context_instance=RequestContext(request))
    else:
        return render_to_response('frontEnd/complete-account-icon.html', context_instance=RequestContext(request))


def host_center(request):
    try:
        username = request.session['username']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True})

    try:
        host = Host.objects.get(username=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')
    if not request.method == 'POST':   # 当使用get请求来请求网页的时候(不带任何的数据请求网页)

        return render_to_response('frontEnd/rent-item.html', {'user': host})

    return render_to_response('frontEnd/rent-item.html')


'''def database(request):
    user = User(username='xxx', password='xxx')
    user.save()
    return HttpResponse('ddfdfd')'''
