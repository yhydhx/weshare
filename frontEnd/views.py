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
from tools import *
from gt.settings import EMAIL_HOST_USER
import json
import chunk
import os
import base64
import time
from urllib import urlencode, unquote
import urllib2
import logging
from gt.settings import SALT, TENCENT_APPID, TENCENT_APPKEY, WEIBO_APPKEY, WEIBO_SECRET, WECHAT_APPID, WECHAT_SECRET


def index(request):
    log = logging.getLogger(__name__)
    provinces = Province.objects.all()
    d = {}
    for s_province in provinces:
        d[s_province.p_name] = {}
        d[s_province.p_name]['name'] = s_province.p_name
        d[s_province.p_name]['id'] = s_province.p_id
        d[s_province.p_name]['schools'] = []

    schools = School.objects.all()
    for s_school in schools:
        if s_school.s_display_index == 0:
            continue
        s_school_name = s_school.s_name
        d_school = {}
        d_school['name'] = s_school_name
        d_school['id'] = s_school.id
        d[s_school.s_province]['schools'].append(d_school)

    obj = []
    for t in d.values():
        obj.append(t)

    # get recommended hosts

    recommend_host = Host()
    Info = {}
    Info = recommend_host.get_all_classes()
    Info.update(recommend_host.get_index_statistic())

    Info['object'] = obj
    
    Info['data'] = {}


    Info['data']['school_on_index_list'] = []
    #get some school on index
    uestc = School.objects.get(id = "57a5a16fd3486d8aedd93a30").format_dict()
    Info['data']['school_on_index_list'].append(uestc)

    login_flag = False


    try:
        # check the user is login or not
        req_username = request.session['email']
        # get the user
        user = Host.objects.get(email=req_username)
        login_flag = True
        return render_to_response('frontEnd/index.html', {'current_user': user,
                                                          'login_flag': login_flag}, Info)
    except:
        return render_to_response('frontEnd/index.html', Info)


@csrf_exempt
def init_register(request):  # 暂时统一用用户名注册,以后的一些坑以后再填
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

        # check blank info
        if not (username and password and password_confirm and phone and email):
            Info['state'] = 400
            Info['message'] = "信息不完整"
        # check the password is the same or not
        elif password_confirm != password:
            Info['state'] = 401
            Info['message'] = "两次密码输入要相同"
        elif not process_mail(email):
            Info['state'] = 402
            Info['data']['email'] = ""
            Info['message'] = '请使用正确格式的邮箱'
        elif not process_passwd(password):
            Info['state'] = 403
            Info['message'] = '请使用正确要求的密码'
        elif not process_phone_num(phone):
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
                try:
                    # 拥有qq_openid注册
                    openid = request.session['openid']
                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                education=-1,
                                register_time=datetime.datetime.now(),
                                icon=DEFAULT_ICON,
                                open_id=openid,
                                )
                    # encode password
                    host.password = host.encode_password(password)
                    host.save()
                    return render_to_response('frontEnd/login.html', context_instance=RequestContext(request))
                except:

                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                education=-1,
                                register_time=datetime.datetime.now(),
                                icon=DEFAULT_ICON,
                                )
                    # encode password
                    host.password = host.encode_password(password)
                    host.save()
                    return render_to_response('frontEnd/login.html', context_instance=RequestContext(request))
        return render_to_response('frontEnd/account.html', Info,
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('frontEnd/account.html', {'error': False}, context_instance=RequestContext(request))


def __checkin__(request):
    try:
        request.session['username']
    except KeyError, e:
        print "KeyError"
        return HttpResponseRedirect('/login/')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            email = request.POST['email']
            password = request.POST['password']
            host = Host()
            password = host.encode_password(password)
            try:
                user = Host.objects.get(email=email)

                if user.password != password:
                    return HttpResponse('用户名或者密码不正确,或者账户处于被冻结的状态')
                else:
                    request.session['email'] = email
                    return HttpResponseRedirect('/index/')
            except:
                return HttpResponse('用户名或者密码不正确,或者账户处于被冻结的状态')
    else:
        return render_to_response('frontEnd/login.html', {'session_timeout': False},
                                  context_instance=RequestContext(request))


def logout(request):
    del request.session['email']
    return HttpResponseRedirect('/index/')


@csrf_exempt
def wechat_login(request):
    try:
        f = open("wechat_test.txt", "a+")
        f.write("============wechat start===========\n")
        code = request.GET['code']
        f.write('code: ' + code + '\n')

        access_token_req_dict = {
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
        }

        address_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' + urlencode(access_token_req_dict)
        f.write('address_token_url: ' + address_token_url + '\n')

        access_token_ret = urllib2.urlopen(address_token_url).read()
        f.write('access_token_url: ' + access_token_ret + '\n')

        access_token_dict = json.loads(access_token_ret)
        access_token = access_token_dict['access_token']
        expires_in = access_token_dict['expires_in']
        openid = access_token_dict['openid']
        scope = access_token_dict['scope']

        tmp_dict = {
            'access_token': access_token,
            'openid': openid,
        }
        address3 = 'https://api.weixin.qq.com/sns/userinfo?' + urlencode(tmp_dict)

        wx_user_info = urllib2.urlopen(address3).read()

        wx_user = json.loads(wx_user_info)
        nickname = wx_user['nickname']
        openid = wx_user['openid']
        headimgurl = wx_user['headimgurl']

        f.write('wx_user_info: ' + wx_user_info + '\n')
        f.close()

        current_user = TmpUser(username=nickname, icon=headimgurl)
        return render_to_response('frontEnd/account.html', {'login_flag': True, 'current_user': current_user},
                                  context_instance=RequestContext(request))
    except:
        f = open("wechat_test.txt", "a+")
        f.write('login failure')
        f.close()
        return HttpResponse("login failure")



@csrf_exempt
def weibo_login(request):
    try:
        f = open('test_wb', 'a+')
        code = request.GET['code']
        f.write('===================weibo start!==================' + '\n')
        f.write('code: ' + code + '\n')

        wdict = {'grant_type': 'authorization_code',
                 'client_id': WEIBO_APPKEY,
                 'client_secret': WEIBO_SECRET,
                 'code': code,
                 'redirect_uri': 'http://www.wshere.com/wblogin/'}

        access_token_url = 'https://api.weibo.com/oauth2/access_token'

        ret_token = post(access_token_url, wdict)
        f.write('ret_weibo_token: ' + str(ret_token) + '\n')

        ret_weibo_token = json.loads(ret_token)

        access_token = ret_weibo_token['access_token']
        expires_in = ret_weibo_token['expires_in']
        remind_in = ret_weibo_token['remind_in']
        uid = ret_weibo_token['uid']

        user_token = {'access_token': access_token, 'uid': uid}
        address2 = 'https://api.weibo.com/2/users/show.json?' + urlencode(user_token)
        user_info = json.loads(urllib2.urlopen(address2).read())
        f.write('user_info[important]: ' + str(user_info) + '\n')

        id = user_info['id']
        username = user_info['name']
        icon = user_info['profile_image_url']

        weibo_user = TmpUser(username=username, icon=icon)
        f.close()
        return render_to_response('frontEnd/account.html', {'login_flag': True, 'current_user': weibo_user},
                                  context_instance=RequestContext(request))

    except IOError:
        f = open('test_wb', 'a+')
        f.write("=============boom in log in=========")
        f.close()
        return None


@csrf_exempt
def qq_login(request):
    Info = {}
    ##########处理qq登录#######
    try:
        f = open('test_v.txt', 'a+')

        code = request.GET['code']
        f.write('code: ' + code + '\n')

        qdict = {'grant_type': 'authorization_code',
                 'client_id': TENCENT_APPID,
                 'client_secret': TENCENT_APPKEY,
                 'code': code,
                 'redirect_uri': 'http://www.wshere.com/qqlogin/'}
        f.write('qdict: ' + str(qdict) + '\n')

        address = 'https://graph.qq.com/oauth2.0/token?' + urlencode(qdict)
        f.write('address: ' + address + '\n')

        ret_qq_token = urllib2.urlopen(address).read()
        f.write('ret_qq_token: ' + ret_qq_token + '\n')

        ret_token = urlencode2dict(str(ret_qq_token))  # ret_token is a dict
        f.write('ret_token: ' + str(ret_token) + '\n')

        access_token = ret_token['access_token']
        f.write('access_token: ' + access_token + '\n')

        # 获取用户的open_ID:
        access_token_dict = {'access_token': access_token}
        f.write('access_token_dict: ' + str(access_token_dict) + '\n')

        address_2 = 'https://graph.qq.com/oauth2.0/me?' + urlencode(access_token_dict)
        f.write('address_2: ' + address_2 + '\n')

        ret_open_id = urllib2.urlopen(address_2).read()
        f.write('ret_open_id: ' + str(ret_open_id) + '\n')  # callback 返回包

        callback_dict = json.loads(str(ret_open_id).split(' ')[1])  # unicode 类型
        f.write('callback_dict: ' + str(callback_dict) + '\n')

        open_id = callback_dict[u'openid']
        f.write('open_id: ' + str(open_id) + '\n')

        try:
            user = Host.objects.get(open_id=open_id)  # 已经有了
            return render_to_response('frontEnd/index.html', Info, {'current_user': user,
                                                                    'login_flag': True})
        except:

            request_dict = {'access_token': access_token,
                            'oauth_consumer_key': TENCENT_APPID,
                            'openid': open_id}
            f.write('request_dict: ' + str(request_dict) + '\n')
            address_3 = 'https://graph.qq.com/user/get_user_info?' + urlencode(request_dict)

            ret_user_info = urllib2.urlopen(address_3).read()
            f.write('ret_user_info: ' + ret_user_info + '\n')

            user_info = json.loads(ret_user_info)
            f.write('user_info: ' + str(user_info) + '\n')

            f.write('###############end##################')

            qq_user = TmpUser(user_info['nickname'], user_info['figureurl_qq_1'])
            f.close()

            request.session['openid'] = open_id
            return render_to_response('frontEnd/account.html', {'login_flag': True, 'current_user': qq_user},
                                      context_instance=RequestContext(request))

    except:
        f = open('test_v.txt', 'a+')
        f.write('did not get the code')
        f.close()
        return None


@csrf_exempt
def i_forget(request, attr=False):
    if not request.method == 'POST':

        # 处理密码找回工作
        if attr:
            print 'attr found' + '  ' + str(attr)
            try:
                forget = Forget.objects.get(forget_string=str(attr))
                print 'forget_object find'
                host = Host.objects.get(id=forget.user_id)
                print 'host find'
                time_now = timezone.datetime.now()
                print 'time marked'
                if (time_now - forget.timestamp).seconds <= 1800:
                    request.session['email'] = host.email
                    return HttpResponseRedirect('/ichange/')
                else:
                    return HttpResponse('您验证的时间过期了,请重新发送验证邮件')
            except:
                return HttpResponse('attr没找到相应的东西')

        # 处理页面显示工作
        else:
            return render_to_response('frontEnd/iforget.html')

    # 处理上传的东西
    else:
        try:
            email = request.POST.get("data", None)
            try:
                host = Host.objects.get(email=email)  # 找到host
                print host
                #  生成找回链接
                print 'host has found'

                string = hashlib.md5(
                    str(email) + str(timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))).hexdigest()
                print string
                forget = Forget(user_id=host.id,
                                forget_string=str(string),
                                timestamp=timezone.datetime.now())
                forget.save()
                print 'forger_object has been found'

                iforget_link = '127.0.0.1:8077/iforget/' + str(string) + '/'
                print iforget_link
            except:
                return HttpResponse('没找到对应的用户,请检查您输入的email')
        except:
            return HttpResponse("后台没有接受到数据")

        '''#######################################
        mail = Mail(
            subject='weshere账户密码找回,请不要回复此邮件',
            from_email=EMAIL_HOST_USER,
            to_email=email,
            host_id=host.id,
            admin_id='1',
            content=iforget_link,
        )
        # mail.sendMail()
        ######################################
        return HttpResponse('邮件已经发送啦')'''


def ichange(request):
    try:
        email = request.session['email']
    except:
        return HttpResponse('没有找到您的session')  # 之后改为404错误
    try:
        user = Host.objects.get(email=email)
    except:
        return HttpResponse('没有找到您所持有的session所对应的用户')
    ERROR = []
    MARK = []
    if request.method == 'POST':
        if request.POST['new-passwd'] and request.POST['new-passwd-confirm']:
            new_password = request.POST['new-passwd']
            new_password_confirm = request.POST['new-passwd-confirm']
            if new_password != new_password_confirm:
                PASSWORD_CONFIRM_ERROR = True
                return render_to_response('frontEnd/ichange.html', {'current_user': user,
                                                                    'PASSWORDCONFIRMERROR': PASSWORD_CONFIRM_ERROR})
            else:
                user.password = new_password
                user.save()
                return render_to_response('frontEnd/ichange.html', {'current_user': user,
                                                                    'change_mark': True})
    else:
        return render_to_response('frontEnd/ichange.html', {'current_user': user})


@csrf_exempt  # 所有有这个东西的全部要删掉到时候重新部署csrf防跨站
def complete_account(request):
    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True},
                                  context_instance=RequestContext(request))
    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('你所持有的session并不在数据库中找到对应内容')

    if request.method == 'POST':
        if request.POST['self-introduction'] and request.POST['birth'] and request.POST['gender'] and request.POST[
            'motto'] and \
                request.POST['min-payment'] and request.POST['service-time'] and request.POST['max-payment'] and \
                request.POST['qq']:

            self_introduction = request.POST['self-introduction']
            gender = request.POST['gender'] 
            motto = request.POST['motto']
            min_payment = float(request.POST['min-payment'])
            service_time = request.POST['service-time']
            max_payment = float(request.POST['max-payment'])
            qq = request.POST['qq']
            alipay = request.POST['alipay']
            birth = request.POST['birth']
            # Education Infomation
            education = request.POST['education']

            try:
                bachelor = request.POST['schoolID1']
                bachelor_major = request.POST['bachelor_major']
                bachelor_start = request.POST['bachelor_major']
                bachelor_end = request.POST['bachelor_end']
            except:
                bachelor = ""
                bachelor_major = ""
                bachelor_start = ""
                bachelor_end = ""
            try:
                graduate = request.POST['schoolID2']
                graduate_major = request.POST['graduate_major']
                graduate_start = request.POST['graduate_start']
                graduate_end = request.POST['graduate_end']
            except:
                graduate = ""
                graduate_major = ""
                graduate_start = ""
                graduate_end = ""
            try:
                phd_major = request.POST['schoolID3']
                phd = request.POST['phd']
                phd_start = request.POST['phd_start']
                phd_end = request.POST['phd_end']
            except:
                phd_major = ""
                phd = ""
                phd_start = ""
                phd_end = ""

            if not judge_limit(min_payment, max_payment):
                return HttpResponse('最低报酬要小于最高报酬')

            host.gender = gender
            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment
            host.birth  = birth
            host.state = HOST_STATE['APPLY']
            host.qq_number = qq

            host.education = education
            host.bachelor = bachelor
            host.graduate = graduate
            host.phd = phd
            host.alipay = alipay
            host.bachelor_major = bachelor_major
            host.graduate_major = graduate_major
            host.phd_major = phd_major
            host.bachelor_start  = bachelor_start
            host.graduate_start  = graduate_start
            host.phd_start  = phd_start

            host.bachelor_end  = bachelor_end
            host.graduate_end  = graduate_end
            host.phd_end  = phd_end

            host.save()
            return HttpResponseRedirect('/complete-account-feature')
        else:
            return HttpResponse('请把表单填写完整')
    else:
        return render_to_response('frontEnd/complete-account.html',
                                  {'login_flag': True,
                                   'current_user': host},
                                  context_instance=RequestContext(request))


''' class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField() '''


@csrf_exempt
def complete_account_feature(request):
    Info = {}

    Info['data'] = {}
    Info['state'] = 0
    Info['message'] = ""

    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True})
    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的session和不能匹配任何一个用户')

    if request.method == 'POST':
        '''
        renew the feature
        '''
        topic_id = request.POST.get('topic_id')
        feature_name = request.POST.get("feature_name")
        host_id = host.id
        showTag = request.POST.get("topic_tag")
        m_id = request.POST.get("minor_topic_id")
        # check this feature is exist or not
        try:
            feature = Feature.objects.get(f_name=feature_name,
                                          f_topic=topic_id)
        except:
            feature = Feature(f_name=feature_name,
                              f_topic=topic_id)
            feature.save()

        # check the error
        if m_id == "":
            Info['state'] = 404
            Info['message'] = "找不到这个小话题"
            return HttpResponse(json.dumps(Info), content_type="application/json")

        # check this is exist or not 
        try:
            Host_Topic.objects.get(host_id=host.id,
                                   t_id=topic_id,
                                   f_id=feature.id,  # 然后把id相互关联起来
                                   m_id=m_id)
            Info['state'] = 300
            Info['message'] = "这个特征已经存在，请添加其他的特征"
            return HttpResponse(json.dumps(Info), content_type="application/json")
        except:
            host_topic = Host_Topic(
                host_id=host.id,
                t_id=topic_id,
                f_id=feature.id,  # 然后把id相互关联起来
                m_id=m_id
            )
        # get the m_name and save the relationship
        try:
            m_name = Minor_Topic.objects.get(id=m_id).m_name
            host_topic.save()
        except:
            Info['state'] = 303
            Info['message'] = "保存信息失败"
            return HttpResponse(json.dumps(Info), content_type="application/json")

        Info['data']['topic_tag'] = showTag
        Info['data']['feature_name'] = feature_name
        Info['data']['m_id'] = m_id
        Info['data']['m_name'] = m_name

        return HttpResponse(json.dumps(Info), content_type="application/json")

    else:
        '''
        show the list
        '''

        topics = Topic.objects.all()
        feature = Feature()
        user_features = feature.get_one_user_features_with_all_topic(host.id)

        Info = {}
        Info['user_features'] = user_features
        Info['host'] = host,
        Info['current_user'] = host
        Info['login_flag'] = True

        # return HttpResponse(json.dumps(Info))
        return render(request, 'frontEnd/complete-account-feature.html', Info)


@csrf_exempt
def delete_feature(request):
    Info = {}
    Info['state'] = 0
    Info['message'] = ""
    Info['data'] = {}

    try:
        username = request.session['email']
        host = Host.objects.get(email=username)
    except:
        Info['state'] = 404
        Info['message'] = "对不起，您尚未登录！"
        return HttpResponse(json.dumps(Info), content_type="application/json")

    if request.method == 'POST':
        '''
        renew the feature
        '''

        topic_id = request.POST.get('topic_id')
        feature_name = request.POST.get("feature_name")
        host_id = host.id
        m_id = request.POST.get("minor_topic_id")

        # check this feature is exist or not

        # find and delete the feature
        try:
            feature = Feature.objects.get(f_name=feature_name, f_topic=topic_id)
            host_topic = Host_Topic.objects.get(
                host_id=host.id,
                t_id=topic_id,
                f_id=feature.id,
                m_id=m_id
            ).delete()
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个feature"
            return HttpResponse(json.dumps(Info))

        Info = {}

        Info['data'] = {}
        Info['data']['topic_id'] = topic_id
        Info['data']['feature_name'] = feature_name
        Info['data']['m_id'] = m_id
        Info['data']['f_id'] = feature.id
        Info['state'] = 0
        Info['message'] = "删除成功"
        return HttpResponse(json.dumps(Info))
    else:
        Info = {}
        Info['state'] = 303
        Info['message'] = "操作错误，本次操作已被记录"
        Info['data'] = {}
        return HttpResponse(json.dumps(Info))


def modify_account(request):
    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'seesion_out': True})
    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')
    if request.method == 'POST':
        if request.POST['username'] and request.POST['phone'] and request.POST[
            'self-introduction'] and request.POST['birth'] and request.POST['gender'] and request.POST[
            'motto'] and \
                request.POST['min-payment'] and request.POST['service-time'] and request.POST['max-payment'] and \
                request.POST['school'] and request.POST['qq']:
            username = request.POST['username']
            phone = request.POST['phone']
            self_introduction = request.POST['self-introduction']
            gender = request.POST['selectbox']
            motto = request.POST['motto']
            min_payment = float(request.POST['min-payment'])
            service_time = request.POST['service-time']
            max_payment = float(request.POST['max-payment'])
            school = request.POST['school']
            qq = request.POST['qq']

           
            if not judge_limit(min_payment, max_payment):
                return HttpResponse('最低报酬要小于最高报酬')

            if gender == u'1':
                host.gender = 0
            elif gender == u'2':
                host.gender = 1

            host.username = username
            host.phone_number = phone
            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment
            host.h_school = school
            host.qq_number = qq
            host.save()
            return render_to_response('frontEnd/modify-account.html', {'login_flag': True,
                                                                       'current_user': host},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse('请把表单填写完整')

    else:
        return render_to_response('frontEnd/modify-account.html', {'current_user': host,
                                                                   'login_flag': True},
                                  context_instance=RequestContext(request))


@csrf_exempt
def image_receive(request):
    try:
        username = request.session['email']
    except:
        render_to_response('frontEnd/login.html', {'session_timeout': True})

    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')

    if request.method == 'POST':
        try:
            data = request.POST.get("data", None)
        except:
            return HttpResponse('data为空')

        processed_data = str(data).split('/jpeg;base64,')[1].split('); background-position: 50% 50')[0]
        processed_pic = base64.b64decode(processed_data)
        mark_list = hashlib.new('md5', timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S")).hexdigest()
        des_origin_path = settings.UPLOAD_PATH + 'icons/' + mark_list + '.jpeg'  # mark_list是唯一的标志
        try:
            des_origin_file = open(des_origin_path, 'w')
            des_origin_file.write(processed_pic)
            des_origin_file.close()
            host.icon = '/files/icons/' + mark_list + '.jpeg'
            host.save()
        except:
            # maybe the picture is too big
            return render(request, 'frontEnd/error.html')

        return HttpResponse('ACKACK')
    else:
        return render_to_response('frontEnd/complete-account-icon.html', {'login_flag': True,
                                                                          'current_user': host},
                                  context_instance=RequestContext(request))


def about(request):
    return render(request, "frontEnd/about.html")


def recruit(request, method, Oid):
    if method == "index":
        return render(request, "frontEnd/recruitment.html")
    else:
        return render(request, "frontEnd/recruit" + method + ".html")


def service(request):
    menu = Menu.objects.filter(m_index=2).order_by("m_upload_time")
    # for k in menu:
    #     print k.id, k.m_name
    services = Document.objects.all().order_by('d_index')
    menu_list = []

    d_topic_question = {}
    for menu_atom in menu:
        menu_list.append(menu_atom.id)
        d_topic_question[menu_atom.id] = {}
        d_topic_question[menu_atom.id]['doc'] = []
        d_topic_question[menu_atom.id]['name'] = menu_atom.m_name

    count = 0
    for service_atom in services:

        if service_atom.d_menu in menu_list:
            count += 1
            service_atom.num = "collapes" + str(count)
            d_topic_question[service_atom.d_menu]['doc'].append(service_atom)

    result = []
    for k in menu:
        result.append(d_topic_question[k.id])

    return render(request, "frontEnd/services.html", {"object": result})


def host_center(request, method, Oid):
    Info = {}
    login_flag = False
    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True})


    try:
        host = Host.objects.get(email=username)
        Info['current_user'] = host.format_dict_with_school_name()
        login_flag = True
        Info['login_flag'] = login_flag
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')

    if method == "edit":

        return render(request, "frontEnd/center-edit.html", Info)
    elif method == "edit2":
        return render(request, "frontEnd/center-edit2.html", Info)
    elif method == "manage":
        Info['sent_bills'] = host.get_one_user_host_bills()
        if host.state != HOST_STATE['GUEST']:
            Info['got_bills'] = host.get_one_host_user_bills()

        return render(request, "frontEnd/center-manage.html", Info)
    elif method == "auth":
        if request.method == "POST":
            host_id = host.id
            
            c_name = request.POST.get("c_name")
            c_state = CERTIFICATE_STATE['CERTIFYING']
            c_introduction = request.POST.get("c_introduction")
            c_type = request.POST.get("c_type")
            mark_list = hashlib.new('md5', timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S")).hexdigest()
            
            des_origin_path = settings.UPLOAD_PATH + 'certification/' + mark_list + "." + c_type
            des_origin_f = open(des_origin_path, "ab")
            tmpImg = request.FILES['certification']
            for chunk in tmpImg.chunks():
                des_origin_f.write(chunk)
            des_origin_f.close()
            c_file_path = "/files/certification/" + mark_list + "." + c_type
            certification = Certificate(
                host_id = host_id ,
                c_file_path = c_file_path,
                c_name = c_name,
                c_state = c_state,
                c_introduction = c_introduction
                )
            certification.save()

            return HttpResponseRedirect("/host_center/auth")
        else:
            return render(request, "frontEnd/center-auth.html", Info)
    elif method == "detail":

        return render(request, "frontEnd/center-manage-detail.html", Info)
    elif method == "modify_base_info":
        if request.method == 'POST':
            
            phone_number = request.POST.get("phone")
            gender = request.POST['gender'] 
            motto = request.POST['motto']
            qq = request.POST['qq']
            birth = request.POST.get("birth")
            # Education Infomation
            education = request.POST['education']

            bachelor = request.POST['schoolID1']
            bachelor_major = request.POST['bachelor_major']
            bachelor_start = request.POST['bachelor_start']
            bachelor_end = request.POST['bachelor_end']


            try:
                graduate = request.POST['schoolID2']
                graduate_major = request.POST['graduate_major']
                graduate_start = request.POST['graduate_start']
                graduate_end = request.POST['graduate_end']
            except:
                graduate = ""
                graduate_major = ""
                graduate_start = ""
                graduate_end = ""
            try:
                phd_major = request.POST['phd_major']
                phd = request.POST['schoolID3']
                phd_start = request.POST['phd_start']
                phd_end = request.POST['phd_end']
            except:
                phd_major = ""
                phd = ""
                phd_start = ""
                phd_end = ""

            host.gender = gender
            host.motto = motto

            host.qq_number = qq

            host.education = education
            host.bachelor = bachelor
            host.graduate = graduate
            host.phd = phd
            host.birth = birth
            #host.alipay = alipay
            host.bachelor_major = bachelor_major
            host.graduate_major = graduate_major
            host.phd_major = phd_major

            host.bachelor_start  = bachelor_start
            host.graduate_start  = graduate_start
            host.phd_start  = phd_start

            host.bachelor_end  = bachelor_end
            host.graduate_end  = graduate_end
            host.phd_end  = phd_end

            host.save()
            return HttpResponseRedirect('/host_center/edit')
        else:
            return HttpResponse('请把表单填写完整')

        
    elif method == "modify_host_info":
        if request.method == "POST":
            self_introduction = request.POST['introduction']
            motto = request.POST['motto']
            min_payment = float(request.POST['min-payment'])
            service_time = request.POST['service-time']
            max_payment = float(request.POST['max-payment'])
        
        
            if not judge_limit(min_payment, max_payment):
                return HttpResponse('最低报酬要小于最高报酬')


            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment

            host.save()
            return HttpResponseRedirect("/host_center/modify_host_info")
        else:
            topics = Topic.objects.all()
            feature = Feature()
            user_features = feature.get_one_user_features_with_all_topic(host.id)

            Info = {}
            Info['user_features'] = user_features
            Info['current_user'] = host
            Info['login_flag'] = True
            return render(request, "frontEnd/center-edit2.html", Info)
    else:
        return HttpResponseRedirect('/user/show/' + host.id)


def school(request, method, Oid):
    login_flag = False
    try:
        username = request.session['email']
        host = Host.objects.get(email=username)
        login_flag = True
    except:
        pass

    if method == "show":
        if request.GET.get("schoolID"):
            return HttpResponseRedirect("/school/detail/" + request.GET.get("schoolID"))
        return render(request, "frontEnd/school-search.html")


    elif method == "detail":
        # find the passed host of the school
        school = School()
        school_union, topics = school.get_single_school_detail(Oid)

        Info = {}
        Info['login_flag'] = login_flag
        Info['object'] = school_union
        Info['topics'] = topics
        Info['school'] = School.objects.get(id=Oid)
        Info['allPeople'] = len(school_union)
        if login_flag == True:
            Info['current_user'] = host

        return render(request, "frontEnd/school.html", Info)
    else:
        return render(request, "frontEnd/404.html")


# user view
@csrf_exempt
def user(request, method, Oid):
    login_flag = False
    try:
        username = request.session['email']
        user = Host.objects.get(email=username)
        login_flag = True
    except:
        pass

    if method == "show":
        try:
            host = Host.objects.get(id=Oid)
        except:
            return render(request, "frontEnd/404.html")

        features = host.get_all_features()
        host.features = features.values()
        host.image = "/files/icons/" + host.icon.split("/")[-1]
        f = Feature()
        questions = f.get_one_host_questions(Oid)

        Info = {}
        Info['host'] = host
        Info['msgs'] = host.get_user_message(host.id)
        Info['questions'] = questions

        if login_flag:
            Info['current_user'] = user
        Info['login_flag'] = login_flag

        return render(request, 'frontEnd/host-index.html', Info)

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

# user view
@csrf_exempt
def share(request, method, Oid):
    login_flag = False
    try:
        username = request.session['email']
        user = Host.objects.get(email=username)
        login_flag = True
    except:
        pass

    Info = {}
    Info['login_flag'] = login_flag
    if login_flag == True:
        Info['current_user'] = user

    if method == "show":
        topic = Topic()
        topics = topic.get_all_topics()
        Info["topics"] = topics
        SHOW_PEOPLE = 20
        SORT_KEY_WORD = ""
        #setting the begin and end
        if request.GET.get("page")== None:
            begin = 0
            end = begin + SHOW_PEOPLE
        else:
            try:
                page = int(request.GET.get("page"))
            except:
                return render("frontEnd/error.html")
            begin = 0 * (page-1)*SHOW_PEOPLE
            end = begin + SHOW_PEOPLE
        if request.GET.get("sortword") != None:
            SORT_KEY_WORD = request.GET.get("sortword")

        if request.method == "POST":
            m_id = request.POST.get("m_id")
            m_name = request.POST.get("m_name")
            t_name = request.POST.get("t_name")

            host_topic = Host_Topic()
            share_hosts = host_topic.get_host_via_minor_topic(m_id)
            request.session["share_hosts"] = share_hosts
            request.session["m_name"] = m_name
            request.session["t_name"] = t_name
            Info['m_name'] = m_name
            Info['t_name'] = t_name
            host_number = len(share_hosts)
            if end < host_number:
                Info['hosts'] = share_hosts[begin:end]
            else:
                Info['hosts'] = share_hosts[:SHOW_PEOPLE]

            #排序
            if SORT_KEY_WORD != "":
                Info['hosts'] =  sorted(Info['hosts'],key= lambda x:x[SORT_KEY_WORD], reverse=True)

        else:
            if request.session.has_key("share_hosts"):
                hosts = request.session["share_hosts"]
                Info['m_name'] =request.session["m_name"]
                Info['t_name'] = request.session["t_name"]
            else:
                tmp_host = Host.objects.filter(state=HOST_STATE['HOST'])
                hosts = []
                for host_atom in tmp_host:
                    hosts.append(host_atom.format_dict())
            host_number = len(hosts)
            if end < host_number:
                Info['hosts'] = hosts[begin:end]
            else:
                Info['hosts'] = hosts[:SHOW_PEOPLE]

            if SORT_KEY_WORD != "":
                Info['hosts'] =  sorted(Info['hosts'],key= lambda x:x[SORT_KEY_WORD], reverse=True)


        return render(request, 'frontEnd/host.html', Info)

    elif method == "clear":
        del request.session["share_hosts"] 
        del request.session["m_name"] 
        del request.session["t_name"]
        return HttpResponseRedirect("/share/show/")

    else:
        return render(request, "frontEnd/404.html")

@csrf_exempt
def image_library(request):
    try:
        username = request.session['email']
    except:
        render_to_response('frontEnd/login.html', {'session_timeout': True})

    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')

    if request.method == 'POST':
        try:
            file = request.FILES['pic-library']
        except:
            return HttpResponse('fail')

        mark_list = hashlib.new('md5', timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S")).hexdigest()
        des_origin_path = settings.UPLOAD_PATH + 'image-library/' + mark_list + '.jpeg'  # mark_list是唯一的标志
        des_origin_file = open(des_origin_path, 'wb')
        des_origin_file.write(file)
        des_origin_file.close()

        user_data = User_data()
        user_data.host_id = host.id
        User_data.url = des_origin_path
        user_data.save()
        return HttpResponse('ACKACK')
    else:  # 来获取图片
        user_data_list = User_data.objects.filter(host_id=host.id)
        index = 1
        url_list = {}
        for user_data in user_data_list:
            user_data[str(index)] = user_data.url
        url_list_json = json.loads(url_list)
        return HttpResponse(url_list_json)


def general_search(request):
    Info = {}
    Info['state'] = 0
    Info['message'] = 0
    Info['data'] = {}

    word_1 = request.GET.get("word_1")
    word_2 = request.GET.get("word_2")

    h = Host()
    search_result = h.general_search(word_1, word_2)
    Info['data']['search_result'] = search_result
    Info['data']['search_number'] = len(search_result)

    if len(search_result == 0):
        Info['state'] = 404
        Info['message'] = "找不到包含关键字的内容"

    return HttpResponse(json.dumps(search_result), content_type="application/json")




'''
@csrf_exempt
def feature_ajax(request):
    try:
        username = request.session['email']
    except:
        return HttpResponse('None')

    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')

    if request.method == 'POST':
        if request.POST.get['type'] == 'add':

        elif request.POST.get['type'] == 'del':
            pass
        else:
            return HttpResponse('no type received')



def database(request):
    user = User(username='xxx', password='xxx')
    user.save()
    return HttpResponse('ddfdfd')'''
