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

    return HttpResponse(json.dumps(Info))




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
        except:
            login_flag = 0

        features = host.get_all_features()
        host.features = features.values()
        host.image = "/files/icons/" + host.icon.split("/")[-1]

        Info['data']['user'] = host.format_dict()
        Info['data']['user']['features'] = features.values()
        Info['data']['msgs'] = host.get_user_message(host.id)
        Info['data']['current_user'] = user.format_dict()
        Info['data']['login_flag'] = login_flag

        return HttpResponse(json.dumps(Info))

    elif method == 'register':
        if request.method == 'POST':
            username = request.POST['username'] 
            password = request.POST['password']
            password_confirm = request.POST['password-confirm']
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
                    return HttpResponse(json.dumps(Info))

            return HttpResponse(json.dumps(Info))
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
                        return HttpResponse(json.dumps(Info))
                    else:
                        request.session['email'] = email
                        Info['message'] = "登录成功"
                        Info['state'] = 0
                        return HttpResponse(json.dumps(Info))
                except:
                    Info['message'] = '用户名或者密码不正确,或者账户处于被冻结的状态'
                    Info['state'] = 400
                    return HttpResponse(json.dumps(Info))
        else:
            Info['state'] = 303
            Info['message'] = "您的操作失误，本次操作已被记录"
            return HttpResponse(json.dumps(Info))

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
        return HttpResponse(json.dumps(Info))

    elif method == "detail":
        #check if the school is exist
        try:
            school = School().objects.get(id=Oid)
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个学校"
            return HttpResponse(json.dumps(Info))

        # find the passed host of the school
        hosts = Host.objects.filter(state=2, h_school=Oid)
        d_topic_detail = {}
        all_host = []
        for each_host in hosts:
            '''
            format the payment 
            fix the path of the image 
            find all tags:
            tags
            find the topics of this users.
            then construct a dict for topic id -> topic tag and topic name 
            make a list of topic
            finally add each tag to users.

            '''
            tmpHost = {}
            tag = ""
            if each_host.gender == 1:
                tag += "male "
            else:
                tag += "female "

            h_topics = Host_Topic.objects.filter(host_id=each_host.id)

            # classification
            d_host_topic = {}
            for h_topic_atom in h_topics:
                t_id = h_topic_atom.t_id
                f_id = h_topic_atom.f_id
                if not d_topic_detail.has_key(t_id):
                    single_topic = Topic.objects.get(id=t_id)
                    d_topic_detail[t_id] = {}
                    d_topic_detail[t_id]['name'] = single_topic.t_name
                    d_topic_detail[t_id]['tag'] = single_topic.t_tag
                    d_topic_detail[t_id]['number'] = 0
                    d_topic_detail[t_id]['index'] = len(d_topic_detail)
                    d_topic_detail[t_id]['topics'] = {}

                d_topic_detail[t_id]['topics'][each_host.id] = 1
                d_topic_detail[t_id]['number'] = len(d_topic_detail[t_id]['topics'])
                d_host_topic[t_id] = d_topic_detail[t_id]['tag']

                # print d_topic_detail[t_id]['topics']
                # print d_topic_detail[t_id]
                # print each_host.username, d_topic_detail[t_id]['name']
            # complete tags

            for k, v in d_host_topic.items():
                tag = tag + " " + str(v)

            tmpHost = each_host.format_dict()
            tmpHost['image'] = "/files/icons/" + each_host.icon.split("/")[-1]
            tmpHost['min_payment'] = int(each_host.min_payment)
            tmpHost['tag'] = tag
            all_host.append(tmpHost)

        Info = {}
        Info['login_flag'] = login_flag
        Info['object'] = all_host
        Info['topics'] = d_topic_detail.values()
        Info['school'] = School.objects.get(id=Oid).format_dict()
        Info['allPeople'] = len(hosts)

        return HttpResponse(json.dumps(Info))
    else:
        return HttpResponse("not found")


