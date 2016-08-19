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
import datetime
from urllib import urlencode, unquote
import urllib2

SALT = 'hetongshinanshen'
TENCENT_APPID = 101340075
TENCENT_APPKEY = '8a66f6a4a93ef09b970afd245ed8b8fc'


def index(request):
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

        ##########处理qq登录#######
        try:
            code = request.GET['code']
            qdict = {'grant_type': 'authorization_code',
                     'client_id': TENCENT_APPID,
                     'client_secret': TENCENT_APPKEY,
                     'code': code,
                     'redirect_uri': 'http://www.wshere.com'}
            address = 'https://graph.qq.com/oauth2.0/token?'+urlencode(qdict)
            ret_qq_token = urllib2.urlopen(address).read()
            ret_token = urlencode2dict(ret_qq_token)
            return render_to_response('frontEnd/index.html', Info)

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


        #check blank info 
        if not (username and password  and password_confirm and phone  and email ):
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
                            education = -1,
                            )
                #encode password
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
            min_payment = request.POST['min-payment']
            service_time = request.POST['service-time']
            max_payment = request.POST['max-payment']
            qq = request.POST['qq']

            #Education Infomation
            education = request.POST['education'] 
            try:
                bacholor = request.POST['bacholor'] 
                bacholor_major = request.POST['bacholor_major']
            except:
                bacholor = ""
                bacholor_major = ""
            try:
                graduate = request.POST['graduate']
                graduate_major = request.POST['graduate_major'] 
            except:
                graduate = ""
                graduate_major = ""
            try:
                phd_major = request.POST['phd_major']
                phd = request.POST['phd'] 
            except:
                phd_major = ""
                phd = ""
                
            if not judge_limit(min_payment, max_payment):
                return HttpResponse('最低报酬要小于最高报酬')

            host.gender = gender
            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment
            host.h_school = school
            host.state = 1
            host.qq_number = qq

            host.education = education
            host.bacholor = bacholor
            host.graduate = graduate
            host.phd = phd
            host.bacholor_major = bacholor_major
            host.graduate_major = graduate_major
            host.phd_major = phd_major


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

        host_topic = Host_Topic(
            host_id=host.id,
            t_id=topic_id,
            f_id=feature.id,  # 然后把id相互关联起来
            m_id = m_id
        )
        host_topic.save()

        Info = {}

        Info['data'] = {}
        Info['state'] = 0
        Info['message'] = ""

        Info['data']['topic_tag'] = showTag
        Info['data']['feature_name'] = feature_name
        Info['data']['m_id'] = m_id

        return HttpResponse(json.dumps(Info))

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

        #return HttpResponse(json.dumps(Info))
        return render(request, 'frontEnd/complete-account-feature.html', Info)

def delete_feature(request):
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
        
        Info = {}
        Info['state'] = 0
        Info['message'] = ""
        Info['data'] = {}

        #find the host
        try:
            host = Host.objects.get(email=username)
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个host"
            return HttpResponse(json.dumps(Info))
        #find and delete the feature
        try:
            feature = Feature.objects.get(f_name=feature_name,f_topic=topic_id)
            host_topic = Host_Topic.objects.get(
                host_id=host.id,
                t_id=topic_id,
                f_id=feature.id,
                m_id = m_id
            ).delete()
        except:
            Info['state'] = 404
            Info['message'] = "找不到这个feature"
            return HttpResponse(json.dumps(Info))

        Info = {}

        Info['data'] = {}
        Info['data']['topic_tag'] = showTag
        Info['data']['topic_id'] = topic_id
        Info['data']['feature_name'] = feature_name
        Info['data']['m_id'] = m_id
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
            min_payment = request.POST['min-payment']
            service_time = request.POST['service-time']
            max_payment = request.POST['max-payment']
            school = request.POST['school']
            qq = request.POST['qq']

            print gender
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
        des_origin_file = open(des_origin_path, 'w')
        des_origin_file.write(processed_pic)
        des_origin_file.close()
        host.icon = '/files/icons/' + mark_list + '.jpeg'
        host.save()
        return HttpResponse('ACKACK')
    else:
        return render_to_response('frontEnd/complete-account-icon.html', {'login_flag': True,
                                                                          'current_user': host},
                                  context_instance=RequestContext(request))


def about(request):
    return render(request, "frontEnd/about.html")

def recruit(request):
    return render(request, "frontEnd/recruitment.html")


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


def host_center(request,method,Oid):
    Info = {}
    Info['state'] = 0
    Info['message'] = ""
    Info['data'] = {}

    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True})

    try:
        host = Host.objects.get(email=username)
        Info['data']['host'] = host.format_dict()
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')



    if method == "edit":
        return render(request,"frontEnd/center-edit.html",Info)
    elif method == "manage":
        return render(request,"frontEnd/center-manage.html",Info)
    elif method == "auth":
        return render(request,"frontEnd/center-auth.html",Info)
    elif method == "detail":

        return render(request,"frontEnd/center-manage-detail.html",Info)     
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
    if method == "show":
        try:
            host = Host.objects.get(id=Oid)
        except:
            return render(request, "frontEnd/404.html")

        features = host.get_all_features()
        host.features = features.values()
        host.image = "/files/icons/" + host.icon.split("/")[-1]

        Info = {}
        Info['user'] = host
        Info['msgs'] = host.get_user_message(host.id)
        Info['current_user'] = host
        Info['login_flag'] = True

        return render_to_response('frontEnd/host-index.html', Info)

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
    search_result = h.general_search(word_1,word_2)
    Info['data']['search_result'] = search_result

    if len(search_result == 0):
        Info['state'] = 404
        Info['message'] = "找不到包含关键字的内容"
        
    return HttpResponse(json.dumps(search_result),content_type="application/json")



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
