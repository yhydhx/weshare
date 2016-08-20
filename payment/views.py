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
from alipay import *

#确认支付  
def pay(request):  
    # cbid=request.POST.get('id')  

    # try:  
    #     cb=cBill.objects.get(id=cbid)  
    # except ObjectDoesNotExist:  
    #     return HttpResponseRedirect("/err/no_object")  
      
    #如果网关是支付宝  
    # if cb.cbank.gateway=='alipay':  
    #         tn=cb.id  
    #         subject=''  
    #         body=''  
    #         bank=cb.cbank.id  
    #         tf='%.2f' % cb.amount  
    #         url=create_direct_pay_by_user (tn,subject,body,bank,tf)  
    # def create_direct_pay_by_user(tn, subject, body, bank, total_fee):  
    url=create_direct_pay_by_user ("12345","weshare","weshare","","0.01")  
    #如果网关是财付通  
    # elif cb.cbank.gateway=='tenpay':  
    #     pass  
      
    #去支付页面  
    return HttpResponseRedirect(url)  
  
#alipay异步通知  
 
@csrf_exempt  
def alipay_notify_url (request):  
    if request.method == 'POST':  
        if notify_verify (request.POST):  
            #商户网站订单号  
            tn = request.POST.get('out_trade_no')  
            #支付宝单号  
            trade_no=request.POST.get('trade_no')  
            #返回支付状态  
            trade_status = request.POST.get('trade_status')  
            cb = cBill.objects.get(pk=tn)  
              
            if trade_status == 'TRADE_SUCCESS':  
                cb.exe()  
                log=Log(operation='notify1_'+trade_status+'_'+trade_no)  
                log.save()  
                return HttpResponse("success")  
            else:  
                #写入日志  
                log=Log(operation='notify2_'+trade_status+'_'+trade_no)  
                log.save()  
                return HttpResponse ("success")  
        else:  
            #黑客攻击  
            log=Log(operation='hack_notify_'+trade_status+'_'+trade_no+'_'+'out_trade_no')  
            log.save()  
    return HttpResponse ("fail")  
  
#同步通知  
  
def alipay_return_url (request):  
    if notify_verify (request.GET):  
        tn = request.GET.get('out_trade_no')  
        trade_no = request.GET.get('trade_no')  
        trade_status = request.GET.get('trade_status')  
            
        cb = cBill.objects.get(pk=tn)  
        #log=Log(operation='return_'+trade_status+'_'+trade_no)  
        #log.save()  
        return HttpResponseRedirect ("/public/verify/"+tn)  
    else:  
        #错误或者黑客攻击  
        #log=Log(operation='err_return_'+trade_status+'_'+trade_no)  
        #log.save()  
        return HttpResponseRedirect ("/")  
  
  
#外部跳转回来的链接session可能丢失，无法再进入系统。  
#客户可能通过xxx.com操作，但是支付宝只能返回www.xxx.com，域名不同，session丢失。  
def verify(request,cbid):  
    try:  
        cb=cBill.objects.get(id=cbid)  
        #如果订单时间距现在超过1天，跳转到错误页面！  
        #避免网站信息流失  
          
        return render_to_response('public_verify.html',{'cb':cb},RequestContext(request))  
    except ObjectDoesNotExist:  
        return HttpResponseRedirect("/err/no_object")  