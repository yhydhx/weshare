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
from gt.settings import EMAIL_HOST_USER
import json
import chunk
import os
import base64
import time
import datetime
from frontEnd.tools import *



def general_search(request):
    Info = output_init()
    word_1 = request.GET.get("word_1")
    word_2 = request.GET.get("word_2") 

    h = Host()
    search_result = h.general_search(word_1,word_2)
    Info['data']['search_result'] = search_result
    Info['data']['search_number'] = len(search_result)

    if len(search_result) == 0:
        Info['state'] = 404
        Info['message'] = "找不到包含关键字的内容"

    return HttpResponse(json.dumps(Info),content_type="application/json")


def output_init():
    Info = {}
    Info['state'] = 0
    Info['message'] = ""
    Info['data'] = {}
    return Info

def index(request):
    #check user is exist
    Info = output_init()

    login_flag = 0
    try:
        user_email = request.session['email'] 
        host = Host.objects.get(email=user_email)
        login_flag = 1
    except:
        host = Host()
        login_flag = 0

    Info['data']['login_flag'] = login_flag
    Info['data'].update( host.get_all_classes())
    Info['data'].update(host.get_index_statistic())

    return HttpResponse(json.dumps(Info),content_type="application/json")



@csrf_exempt
def user(request, method, Oid):
    Info = output_init()
    if method == "show":
        #check the user is exist or not
        try:
            host = Host.objects.get(id=Oid)
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个用户"
            return HttpResponse(json.dumps(Info))
        #check the user is login or not
        try:
            user = Host.objects.get(email= request.session['email'])
            login_flag = 1
            Info['data']['current_user'] = user.format_dict()
        except:
            login_flag = 0

        features = host.get_all_features()
        host.features = features.values()
        host.image = "/files/icons/" + host.icon.split("/")[-1]

        Info['data']['user'] = host.format_dict()
        Info['data']['user']['features'] = features.values()
        Info['data']['msgs'] = host.get_user_message(host.id)
        Info['data']['login_flag'] = login_flag

        return HttpResponse(json.dumps(Info),content_type="application/json")

    elif method == 'register':
        if request.method == 'POST':
            username = request.POST['username'] 
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            phone = request.POST['phone']
            email = request.POST['email']
            

            Info = {}
            Info['state'] = 0
            Info['message'] = ""
            Info['data'] = {}
            
            Info['data']['username'] = username 
            Info['data']['phone'] = phone 
            Info['data']['email'] = email 


            #check blank info 
            if not (username and password  and password_confirm and phone  and email  ):
                Info['state'] = 400
                Info['message'] = "信息不完整"
            # check the password is the same or not
            elif  password_confirm != password:
                Info['state'] = 401
                Info['message'] = "两次密码输入要相同"
            elif not process_mail(email):
                Info['state'] = 402
                Info['data']['email'] = ""
                Info['message'] = '请使用正确格式的邮箱'
            elif not process_passwd(password):
                Info['state'] = 403
                Info['message'] = '请使用正确要求的密码'
            elif  not process_phone_num(phone):
                Info['state'] = 404
                Info['data']['phone'] = ""
                Info['message'] = '请选择国家区号'
            else:
                try:
                    Host.objects.get(email=email)
                    Info['state'] = 405
                    Info['message'] = '您的邮箱已经被注册了'
                    Info['data']['email'] = ""
                except:
                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                )
                    #encode password
                    host.password = host.encode_password(password)
                    host.save()
                    Info['state'] = 0
                    Info['message'] = "注册成功"
                    return HttpResponse(json.dumps(Info),content_type="application/json")

            return HttpResponse(json.dumps(Info),content_type="application/json")
        else:
            #method = "get"
            Info['state'] = '404'
            Info['message'] = "找不到这个方法"
            return HttpResponse(json.dumps(Info))

    elif method == "login":
        if request.method == 'POST':
            if request.POST['email'] and request.POST['password']:
                host = Host()
                email = request.POST['email']
                password = host.encode_password(request.POST['password'])
                try:
                    user = Host.objects.get(email=email)

                    if user.password != password:
                        Info['state'] = 404
                        Info['message'] = "密码错误"
                        return HttpResponse(json.dumps(Info),content_type="application/json")
                    else:
                        request.session['email'] = email
                        Info['message'] = "登录成功"
                        Info['state'] = 0
                        return HttpResponse(json.dumps(Info),content_type="application/json")
                except:
                    Info['message'] = '用户名或者密码不正确,或者账户处于被冻结的状态'
                    Info['state'] = 400
                    return HttpResponse(json.dumps(Info),content_type="application/json")
        else:
            Info['state'] = 303
            Info['message'] = "您的操作失误，本次操作已被记录"
            return HttpResponse(json.dumps(Info),content_type="application/json")

    elif method == "msg":
        # check whether the user is online
        try:
            req_username = request.session['email']
            # get the user
            user = Host.objects.get(email=req_username)
        except:
            return render(request, "frontEnd/404.html")

        # check is the host exist
        try:
            host = Host.objects.get(id=Oid)
        except:
            return render(request, "frontEnd/404.html")

        # save the message
        msg = request.POST.get("message")
        if user.icon == "":
            user.icon == DEFAULT_ICON

        message = Message(
            from_user=user.id,
            to_user=host.id,
            message_type=0,  # which means normal message
            icon=user.icon,
            content=msg,
            upload_time=datetime.datetime.now(),
        )
        message.save()

        return HttpResponseRedirect("/user/show/" + Oid)


    else:
        return render(request, "frontEnd/404.html")


def register_host(request,method,Oid):
    Info = output_init()
    try:
        username = request.session['email']
        host = Host.objects.get(email=username)
    except:
        Info['state'] = 404
        Info['message'] = "找不到该用户"

    if method == "step1":
        pass



@csrf_exempt
def school(request, method, Oid):
    try:
        user = Host().objects.get(email=request.session['email'])
        login_flag = 1
    except:
        login_flag = 0

    Info = output_init()
    if method == "show":
        s = School()
        result = s.get_country_province_school()
        Info['data']['all_countries'] = result
        return HttpResponse(json.dumps(Info),content_type="application/json")

    elif method == "detail":
        #check if the school is exist
        try:
            school = School.objects.get(id=Oid)
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个学校"
            return HttpResponse(json.dumps(Info),content_type="application/json")

        # find the passed host of the school
        school = School()
        school_union, topics = school.get_single_school_detail(Oid)

        Info = output_init()
        Info['data']['login_flag'] = login_flag
        Info['data']['object'] = school_union
        Info['data']['topics'] = topics
        Info['data']['school'] = school.format_dict()
        Info['data']['allPeople'] = len(school_union)
        if login_flag == True:
            Info['data']['current_user'] = host

        return HttpResponse(json.dumps(Info),content_type="application/json")
    else:
        return HttpResponse("not found")

def test(request):
    Info = output_init()
    Info['test'] = "this is a test"
    Info['data']['a'] = 'b' 
    return HttpResponse(json.dumps(Info),content_type="application/json")

