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
import chunk
import os
import base64


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


    login_flag = False
    try:
        req_username = request.session['email']
    except:
        return render_to_response('frontEnd/index.html')
    try:
        user = Host.objects.get(email=req_username)
        login_flag = True
        return render_to_response('frontEnd/index.html', {'current_user': user,
                                                          'login_flag': login_flag})
    except:
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
                if not process_mail(email):
                    error = '请使用正确格式的邮箱'
                    return render_to_response('frontEnd/account.html', {'error': error},
                                              context_instance=RequestContext(request))
                if not process_passwd(password):
                    error = '请使用正确要求的密码'
                    return render_to_response('frontEnd/account.html', {'error': error},
                                              context_instance=RequestContext(request))
                try:
                    Host.objects.get(email=email)
                    error = '您的邮箱已经被注册了'
                    return render_to_response('frontEnd/account.html', {'error': error},
                                              context_instance=RequestContext(request))
                except:
                    host = Host(username=username,
                                password=password,
                                email=email,
                                phone_number=phone,
                                )
                    host.save()
                    return render_to_response('frontEnd/login.html', context_instance=RequestContext(request))
            else:
                error = '两次密码输入要相同'
                return render_to_response('frontEnd/account.html', {'error': error},
                                          context_instance=RequestContext(request))
        else:
            error = '请填满表单中的每一项'
            return render_to_response('frontEnd/account.html', {'error': error},
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
                request.POST['school'] and request.POST['qq']:
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

            host.introduction = self_introduction
            host.motto = motto
            host.min_payment = min_payment
            host.service_time = service_time
            host.max_payment = max_payment
            host.h_school = school
            host.state = 1
            host.qq_number = qq
            host.save()
            return render_to_response('frontEnd/complete-account-feature.html', {'login_flag': True,
                                                                                 'currrent_user': host})
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
        foreign = ''
        course = ''
        competition = ''
        try:
            foreign = request.POST['foreign']
        except:
            try:
                course = request.POST['course']
            except:
                try:
                    competition = request.POST['competition']
                except:
                    return HttpResponse('请填写表单')

        if foreign:
            feature = Feature()
            topic = Topic()
            host_topic = Host_Topic()  # 先把相关联的对象相关联起来

            try:
                topic = Topic.objects.get(t_name=u'留学咨询')

            except:
                print "could not find the topic"
                topic.t_name = u'留学咨询'
                topic.t_click = 0
                topic.save()

            feature.f_name = foreign
            feature.f_topic = topic.t_name

            feature.save()

            host_topic.host_id = host.id
            host_topic.t_id = topic.id
            host_topic.f_id = feature.id  # 然后把id相互关联起来
            host_topic.save()

        if course:
            feature = Feature()
            topic = Topic()
            host_topic = Host_Topic()  # 先把相关联的对象相关联起来

            try:
                topic = Topic.objects.get(t_name=u'课程咨询')
            except:
                topic.t_name = u'课程咨询'
                topic.t_click = 0
                topic.save()

            feature.f_name = course
            feature.f_topic = topic.t_name

            topic.save()
            feature.save()

            host_topic.host_id = host.id
            host_topic.t_id = topic.id
            host_topic.f_id = feature.id  # 然后把id相互关联起来
            host_topic.save()

        if competition:
            feature = Feature()
            topic = Topic()
            host_topic = Host_Topic()  # 先把相关联的对象相关联起来

            try:
                topic = Topic.objects.get(t_name=u'竞赛经历')
            except:
                topic.t_name = u'竞赛经历'
                topic.t_click = 0
                topic.save()

            feature.f_name = competition
            feature.f_topic = topic.t_name

            topic.save()
            feature.save()

            host_topic.host_id = host.id
            host_topic.t_id = topic.id
            host_topic.f_id = feature.id  # 然后把id相互关联起来
            host_topic.save()

    feature_list_1 = []
    feature_list_2 = []
    feature_list_3 = []

    h_topics = Host_Topic.objects.filter(host_id=host.id)
    print len(h_topics)
    # classification
    d_topic_feature = {}
    for h_topic_atom in h_topics:
        t_id = h_topic_atom.t_id
        f_id = h_topic_atom.f_id
        if not d_topic_feature.has_key(t_id):
            d_topic_feature[t_id] = [f_id]
        else:
            d_topic_feature[t_id].append(f_id)

    print d_topic_feature

    # transform the id into chinese
    d_topic_feature_translate = {}
    for k, v in d_topic_feature.items():
        topic_name = Topic.objects.get(id=k).t_name
        d_topic_feature_translate[topic_name] = []
        for feature_atom_id in v:
            feature_name = get_object_or_404(Feature, id=feature_atom_id).f_name
            d_topic_feature_translate[topic_name].append(feature_name)

    print d_topic_feature_translate

    for topic, feature_list in d_topic_feature_translate.items():
        if topic == u'留学咨询':
            feature_list_1 = feature_list
        elif topic == u'课程咨询':
            feature_list_2 = feature_list
        elif topic == u'竞赛经历':
            feature_list_3 = feature_list

    return render_to_response('frontEnd/complete-account-feature.html', {'feature_list_1': feature_list_1,
                                                                         'feature_list_2': feature_list_2,
                                                                         'feature_list_3': feature_list_3,
                                                                         'host': host,
                                                                         'current_user': host,
                                                                         'login_flag': True},
                              context_instance=RequestContext(request))


def host_center(request):
    try:
        username = request.session['email']
    except:
        return render_to_response('frontEnd/login.html', {'session_timeout': True})

    try:
        host = Host.objects.get(email=username)
    except:
        return HttpResponse('您所持有的用户名不能匹配任何一个host')

    
    features = host.get_all_features()
    host.features =  features.values()
    host.image = "/files/icons/"+host.icon.split("/")[-1]

    return render_to_response('frontEnd/host-index.html', {'user': host,
                                                          'login_flag': True,
                                                          'current_user': host,
                                                          'user': host})


def modify_account(request):
    try:
        username = request.session['email']
        print 1
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
        host.icon = 'files/icons/' + mark_list + '.jpeg'
        host.save()
        return HttpResponse('ACKACK')
    else:
        return render_to_response('frontEnd/complete-account-icon.html', {'login_flag': True,
                                                                          'current_user': host},
                                  context_instance=RequestContext(request))

def about(request):
    return render(request,"frontEnd/about.html")

def service(request):
    menu = Menu.objects.filter(m_index=2)
    services = Document.objects.all()
    menu_list = []

    d_topic_question = {}
    for menu_atom in menu:
        menu_list.append(menu_atom.m_name)
        d_topic_question[menu_atom.m_name] = {}
        d_topic_question[menu_atom.m_name]['doc'] = []
        d_topic_question[menu_atom.m_name]['name'] = menu_atom.m_name

    count = 0    
    for service_atom in services:
        if service_atom.d_menu in menu_list:
            count += 1
            service_atom.num = "collapes"+str(count)
            d_topic_question[service_atom.d_menu]['doc'].append(service_atom)


    return render(request,"frontEnd/services.html",{"object":d_topic_question.values()})

def school(request):
    hosts = Host.objects.all()
    d_topic_detail = {}
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


        tag = ""
        if each_host.gender == 1:
            tag += "male "
        else:
            tag += "female "
        

        h_topics = Host_Topic.objects.filter(host_id=each_host.id)

        #classification
        d_host_topic = {}
        for h_topic_atom in h_topics:
            t_id = h_topic_atom.t_id
            f_id = h_topic_atom.f_id
            if not d_topic_detail.has_key(t_id):    
                single_topic = Topic.objects.get(id = t_id)
                d_topic_detail[t_id] = {}
                d_topic_detail[t_id]['name'] = single_topic.t_name
                d_topic_detail[t_id]['tag'] = single_topic.t_tag
                d_topic_detail[t_id]['number'] = 0
                d_topic_detail[t_id]['index'] = len(d_topic_detail)
                d_topic_detail[t_id]['topics'] = {}

            d_topic_detail[t_id]['topics'][each_host.id] = 1
            d_topic_detail[t_id]['number'] = len(d_topic_detail[t_id]['topics'])
            d_host_topic[t_id] = d_topic_detail[t_id]['tag']
            
            #print d_topic_detail[t_id]['topics']
            #print d_topic_detail[t_id]
            print each_host.username, d_topic_detail[t_id]['name']
        #complete tags
        for k,v in d_host_topic.items():
            tag = tag + " " +v

        

        each_host.image = "/files/icons/"+each_host.icon.split("/")[-1]
        each_host.min_payment = int(each_host.min_payment)
        each_host.tag = tag
    

    Info = {}
    Info['object'] = hosts
    Info['topics'] = d_topic_detail.values()

    Info['allPeople'] = len(hosts)

    return render(request, "frontEnd/school.html",Info)

'''def database(request):
    user = User(username='xxx', password='xxx')
    user.save()
    return HttpResponse('ddfdfd')'''
