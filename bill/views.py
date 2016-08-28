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
from urllib import urlencode, unquote
import urllib2
from payment.alipay import *



def bill(request,method,Oid):
    '''
    订单系统的主页
    '''
    Info = {}
    try:

        username = request.session['email']
        user = Host.objects.get(email=username)
    	login_flag = True
    	Info['current_user'] = user
    	Info['login_flag']  = login_flag
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
            return render(request,"frontEnd/404.html")

		#generate bill id
		#


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
        return HttpResponseRedirect('/host_center/manage')
		

    elif method == "detail":

    	try:
    		appointment = Appointment.objects.get(id = Oid)
    		Info['appointment'] = appointment.format_dict_on_manage()
    	except:
    		return render(request,'frontEnd/404.html')

    	#show the comment 
    	
    	Info['messages'] = appointment.get_appointment_messages()
    	#check this user is the host or not 
    	if user.id == appointment.from_user_id : 
    		return render(request,'frontEnd/appoint_guest.html',Info)
    	elif user.id == appointment.to_host_id :
    		return render(request,'frontEnd/appoint_host.html',Info)

	
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
			return render(request,'frontEnd/error.html')

		#format the time
		try:
			recommend_begin_time = datetime.datetime.strptime(recommend_begin_time, "%Y-%m-%d %H:%M:%S")
			recommend_end_time = datetime.datetime.strptime(recommend_end_time, "%Y-%m-%d %H:%M:%S")
		except:
			return render(request,"frontEnd/error.hmtl")

		Appointment.objects.filter(id=appnt_id).update(
															recommend_info = recommend_info,
														    recommend_begin_time = recommend_begin_time,
														    recommend_end_time = recommend_end_time,
														    recommend_length = recommend_length,
														    recommend_payment = recommend_payment,
														    recommend_salary = recommend_salary,
														    state = APPOINTMENT_STATE.CERTIFIED
														    )
		return HttpResponseRedirect("/host_center/manage")
    elif method == "communicate":
		appnt_id = request.POST.get("appnt_id")
		message = request.POST.get("message")
		

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
		return HttpResponseRedirect('/bill/detail/'+appnt_id)

		try:
			appointment = Appointment.objects.get(id= appnt_id)
			message_type =  MESSAGE_TYPE['APPOINTMENT_COMM']
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
			return HttpResponseRedirect('/bill/detail/'+appnt_id)

		except:
			return render(request,"frontEnd/error.html")
    elif method == "pay":
		try:
			appnt_id = request.POST.get("appnt_id")
			appointment = Appointment.objects.get(id = appnt_id)
			host = Host.objects.get(id= appointment.to_host_id)
		except:
			return render(request,'frontEnd/error.html')


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

		return HttpResponseRedirect(url)

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