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
        Info['data']['current_user'] = host.format_dict()
    except:
        host = Host()
        login_flag = 0

    Info['data']['login_flag'] = login_flag
    Info['data'].update( host.get_all_classes())
    Info['data'].update(host.get_index_statistic())
    Info['schools'] = host.get_index_schools()
    return HttpResponse(json.dumps(Info),content_type="application/json")



@csrf_exempt
def user(request, method, Oid):
    Info = output_init()
    try:
        host = Host.objects.get(email=request.session['email'])
        Info['current_user'] = host.format_dict()
        login_flag = True
        Info['data']['current_user'] = host
    except:
        login_flag = False
    Info['data']['login_flag'] = login_flag

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
            Info['state'] = HOST_STATE['GUEST']
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
                    #check if there is openid 
                    try:
                        open_id = request.POST.get("union_id")
                    except :
                        open_id = ""

                    #check if there is icon 
                    try:
                        icon = request.POST.get("icon")
                    except :
                        icon = ""
                    if icon == "":
                        icon = DEFAULT_ICON

                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                open_id = open_id,
                                icon = icon,
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
                        Info['data']['login_flag'] = 1
                        Info['current_user'] = user
                        return HttpResponse(json.dumps(Info),content_type="application/json")
                except:
                    Info['message'] = '用户名或者密码不正确,或者账户处于被冻结的状态'
                    Info['state'] = 400
                    return HttpResponse(json.dumps(Info),content_type="application/json")
        else:
            Info['state'] = 303
            Info['message'] = "您的操作失误，本次操作已被记录"
            return HttpResponse(json.dumps(Info),content_type="application/json")

    elif method == "qqlogin":
        if request.method == "POST":
            
            try:
                username = request.POST.get("username")
                icon = request.POST.get("icon")
                union_id = request.POST.get("union_id")
            except:
                Info['state'] = 404
                Info['message'] = "操作错误"
                return HttpResponse(json.dumps(Info),content_type="application/json")

            #check our server has this account or not 
            
            try:
                host = Host.objects.get(open_id = union_id)
                #login success

                request.session['email'] = host.email
                Info['data']['registed'] = True
                Info['message'] = "登录成功"
            except:
                Info['message'] = "由于您是第一次登录,请完善部分信息"
                Info['data']['registed'] = False

                Info['data']['username'] = username
                Info['data']['icon'] = icon
                Info['data']['union_id'] = union_id
            return HttpResponse(json.dumps(Info),content_type="application/json")    

        else:
            Info['state'] = 500
            Info['message'] = "您的操作有误，本次操作已经被记录"
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

    elif method == 'logout':
        if request.session.has_key('email'):
            del request.session['email']
            Info['message'] = "登出成功"

        else:
            Info['state'] = 404
            Info['message'] = "您已经登出"
        return HttpResponse(json.dumps(Info),content_type="application/json")

    elif method == "manage_bill":
        Info['data']['sent_bills'] = host.get_one_user_host_bills()
        if host.state != HOST_STATE['GUEST']:
            Info['data']['got_bills'] = host.get_one_host_user_bills()
        return HttpResponse(json.dumps(Info),content_type="application/json")

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

@csrf_exempt
def bill(request,method,Oid):
    '''
    订单系统的主页
    '''
    Info = output_init()
    try:
        username = request.session['email']
        user = Host.objects.get(email=username)
    except:
        Info['state'] = 404
        Info['message'] = "对不起，您尚未登录！"
        return HttpResponse(json.dumps(Info), content_type="application/json")
    #get the host

    if method == "init":

        try:
            feature_id  = request.POST.get("feature_id")
            host_id  = request.POST.get("host_id")
            intro_and_question  = request.POST.get("intro_and_question")    
            appointment_time  = request.POST.get("appointment_time")
            user = Host.objects.get(email = request.session['email'])
            host = Host.objects.get(id = host_id)
        except:
            Info['state'] = 404
            Info['message'] = "对不起，您尚未登录！"
            return HttpResponse(json.dumps(Info), content_type="application/json")

        #generate bill id

        appointment = Appointment(
            state = APPOINTMENT_STATE['INITED'] ,
            from_user_id = user.id,
            to_host_id = host.id,  
            from_user_icon = user.icon,
            to_host_icon = host.icon,
            intro_and_question = intro_and_question,
            appointment_time = appointment_time,
            appointment_id = 1,
            feature_id = feature_id,
            appointment_init_time = datetime.datetime.now(),
        )

        appointment.appointment_id = appointment.generate_id()
        appointment.save()
        
        Info['message'] = "订单创建成功"
        return HttpResponse(json.dumps(Info), content_type="application/json")
        

    elif method == "detail":

        try:
            appointment = Appointment.objects.get(id = Oid)
            Info['data']['appointment'] = appointment.format_dict_on_manage()
            
        except:
            Info['state'] = 404
            Info['message'] = "对不起，该订单不存在！"
            return HttpResponse(json.dumps(Info), content_type="application/json")
            
        #show the comment 
        
        Info['messages'] = appointment.get_appointment_messages()
        #check this user is the host or not 
        if user.id == appointment.from_user_id : 
            Info['user_page'] = True
            Info['message'] = "查询成功，返回用户页面！"
            return HttpResponse(json.dumps(Info), content_type="application/json")
        elif user.id == appointment.to_host_id :
            Info['user_page'] = False
            Info['message'] = "查询成功，返回Host页面！"
            return HttpResponse(json.dumps(Info), content_type="application/json")

    
    elif method == "host_certify":
        try:
            appnt_id = request.POST.get("appnt_id")
            recommend_info = request.POST.get("recommend_info")
            recommend_begin_time = request.POST.get("recommend_begin_time")
            recommend_end_time = request.POST.get("recommend_end_time")
            recommend_length = request.POST.get("recommend_length")
            recommend_payment = request.POST.get("recommend_payment")
            recommend_salary = request.POST.get("recommend_salary")
        except:
            Info['state'] = 404
            Info['message'] = "对不起，该订单不存在！"
            return HttpResponse(json.dumps(Info), content_type="application/json")

        #format the time
        try:
            recommend_begin_time = datetime.datetime.strptime(recommend_begin_time, "%Y-%m-%d %H:%M:%S")
            recommend_end_time = datetime.datetime.strptime(recommend_end_time, "%Y-%m-%d %H:%M:%S")
        except:
            Info['state'] = 303
            Info['message'] = "对不起，时间格式错误！"
            return HttpResponse(json.dumps(Info), content_type="application/json")

        Appointment.objects.filter(id=appnt_id).update(
                                                            recommend_info = recommend_info,
                                                            recommend_begin_time = recommend_begin_time,
                                                            recommend_end_time = recommend_end_time,
                                                            recommend_length = recommend_length,
                                                            recommend_payment = recommend_payment,
                                                            recommend_salary = recommend_salary,
                                                            state = APPOINTMENT_STATE.CERTIFIED
                                                            )
        Info['message'] = "订单修改成功，请客户检查并付款"
        return HttpResponse(json.dumps(Info), content_type="application/json")

    elif method == "communicate":
        appnt_id = request.POST.get("appnt_id")
        message = request.POST.get("message")
        try:
            appointment = Appointment.objects.get(id= appnt_id)
            message_type =  MESSAGE_TYPE.APPOINTMENT_COMM
            new_message = Message(    
                                from_user = user.id,
                                to_user = appointment.to_host_id,
                                message_type = message_type,
                                icon = user.icon,
                                upload_time = datetime.datetime.now(),
                                content = message,
                                extra_id = appnt_id,
                                )
            new_message.save()
            Info['message'] = "信息提交成功"
            return HttpResponse(json.dumps(Info), content_type="application/json")
        except:
            Info['state'] = 500
            Info['message'] = "对不起，提交错误！"
            return HttpResponse(json.dumps(Info), content_type="application/json")

    elif method == "pay":
        try:
            appnt_id = request.POST.get("appnt_id")
            appointment = Appointment.objects.get(id = appnt_id)
            host = Host.objects.get(id= appointment.to_host_id)
        except:
            Info['state'] = 404
            Info['message'] = "对不起,该订单不存在！"
            return HttpResponse(json.dumps(Info), content_type="application/json")


        bill = Bill(
            bill_id = appointment.appointment_id ,      # 请与贵网站订单系统中的唯一订单号匹配  
            subject = u"与"+host.username+u"交流"+str(appointment.recommend_length)+u"小时",     # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。  
            body = u"与"+host.username+u"交流"+str(appointment.recommend_length)+u"小时",           # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空  
            total_fee = appointment.recommend_salary,                  
            create_time = datetime.datetime.now(),
            state =  BILL_STATE.UNPAID,
            from_user_id = appointment.from_user_id,
            to_host_id = appointment.to_host_id,
            bill_type = BILL_TYPE.APPOINTMENT,
        )
        bill.save()

        url=create_direct_pay_by_user (bill.bill_id,bill.subject,bill.body,"",bill.total_fee)  

        Info['state'] = 0
        Info['message'] = "付款链接创建成功！"
        Info['data']['url'] = url
        return HttpResponse(json.dumps(Info), content_type="application/json")

    elif method == "verify":
        '''
            从阿里巴巴返回的数据
        '''
        try:
            bill = Bill.objects.get(bill_id = Oid)
            bill.state = BILL_STATE.PAID
            bill.save()
            appointment = Appointment.objects.get(appointment_id = bill.bill_id)
            appointment.state = APPOINTMENT_STATE.PAID
            appointment.save()
        except:
            return render(request,"frontEnd/error.html")

        return HttpResponseRedirect('host_center/manage')

    elif method == "test":
        return HttpResponse("test")

    else:
        return HttpResponse("end")



def test(request):
    Info = output_init()
    Info['test'] = "this is a test"
    Info['data']['c'] = Appointment.objects.count() 
    return HttpResponse(json.dumps(Info),content_type="application/json")

