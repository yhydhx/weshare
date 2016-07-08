# coding: utf-8  
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, RequestContext
from django.core.urlresolvers import reverse
from django.views import generic

from django import forms

#mail section 
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.template import Context, loader

from gt.models import *
import datetime
from django.utils import timezone
from django.conf import settings
from gt.settings import *



import hashlib

'''def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': 1}
    return render(request, 'backEnd/index.html', context)
'''


def __checkin__(request):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')


def login(request):
    return render(request, 'backEnd/login.html')


def logout(request):
    del request.session['adminname']
    return HttpResponseRedirect("login.html")


def loginCertifacate(request):
    if request.method == 'POST':
        # If the form has been submitted...
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        user = get_object_or_404(Admin, username=username)
        if user.password == password:
            request.session['adminname'] = username
            return HttpResponseRedirect('/dc/province/show/')
        else:
            return HttpResponse("密码错误")


def contact(request):
    '''if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the previous section
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = {'data': 2}
            context = {'latest_poll_list': 1}
            return render(request, 'tt/index.html', {'data':2,
            											'bigcity':2})
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
'''
    if request.method == 'POST':
        username = request.POST.get("username")
        request.session['adminname'] = data
        return HttpResponse(data)
        return render(request, 'backEnd/index.html', {'data': data, 'bigcity': 2})
    else:
        return HttpResponse(request.session['username'])


def addUserView(request):
    return render(request, "backEnd/addUserView.html")


def addUser(request):
    md5Encode = hashlib.new("ripemd160")
    username = request.POST.get("username")
    tmpPassword = request.POST.get("password")
    confirmPassword = request.POST.get("password2")
    if tmpPassword != confirmPassword:
        return HttpResponse("两次输入的密码不一致")
    md5Encode.update(tmpPassword)
    password = md5Encode.hexdigest()

    veryfyUser = Admin.objects.filter(username=username).all()

    try:
        HttpResponse(veryfyUser[0])
    except IndexError, e:
        veryfyUser = None
    if veryfyUser is not None:
        return HttpResponse("This user is already exits")

    user = Admin(
        username=username,
        password=password
    )
    user.save()
    return render(request, "backEnd/login.html")


def changePasswd(request):
    if request.method == "POST":
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        newPassword = request.POST.get("newPassword")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        user = get_object_or_404(Admin, username=username)
        if user.password == password:
            newEncode = hashlib.new("ripemd160")
            newEncode.update(newPassword)
            user.password = newEncode.hexdigest()
            user.save()
            del request.session['adminname']
            return HttpResponseRedirect("login.html")
        else:
            return HttpResponse("密码错误")

    else:
        return render(request, "backEnd/changePasswd")


def index(request):
    return render(request, 'backEnd/index2.html', {'news': News.objects.all()})
    return render(request, 'backEnd/index2.html')


########################################################
# this view is about the news 
# contains show news list , add news , change news, 
# delete news,and add new news
# News contain three parts , title content date                 
########################################################
def province(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addProvince':
        name = request.POST.get('province_name')
        p_id = request.POST.get('province_id')

        province = Province(
            p_name=name,
            p_id=int(p_id),
        )
        province.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/province/show/')
    elif method == 'change':
        return render(request, 'backEnd/changeProvince.html', {'object': Province.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            province = {'p_name': request.POST.get('province_name'),
                        'p_id': request.POST.get('province_id'),
                        'id': request.POST.get("id")
                        }
            Province.objects.filter(id=province['id']).update(p_name=province['p_name'], p_id=province['p_id'])

        return HttpResponseRedirect('/dc/province/show')

    elif method == 'delete':
        Province.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request, 'backEnd/addProvinceView.html')
    elif method == 'show':
        # return HttpResponse("hello")
        return render(request, 'backEnd/showProvinceList.html', {'object': Province.objects.all()})
    else:
        return HttpResponse('没有该方法')


def school(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')

    if method == 'addSchool':
        s_name = request.POST.get("s_name")
        p_name = request.POST.get("p_name")
        s_display_index = request.POST.get("s_display_index")
        school = School(
            s_name=s_name,
            s_province=p_name,
            s_student_number=0,
            s_display_index=s_display_index,
        )
        school.save()

        return HttpResponseRedirect('/dc/school/show')
    elif method == 'change':
        school = School.objects.get(id=Oid)
        provinces = Province.objects.all()
        return render(request, 'backEnd/changeSchool.html', {'school': school, 'provinces': provinces})

    elif method == 'save':
        if request.method == 'POST':
            school = {'s_name': request.POST.get('s_name'),
                      's_province': request.POST.get("p_name"),
                      'id': request.POST.get("id"),
                      's_display_index': request.POST.get("s_display_index")
                      }

        School.objects.filter(id=school['id']).update(s_name=school['s_name'],
                                                      s_province=school['s_province'],
                                                      s_display_index=school['s_display_index']
                                                      )

        return HttpResponseRedirect('/dc/school/show')

    elif method == 'delete':
        School.objects.filter(id=Oid).delete()

        return HttpResponseRedirect('../show')
    elif method == 'add':
        provinces = Province.objects.all()
        return render(request, 'backEnd/addSchoolView.html', {'provinces': provinces})
    elif method == 'show' or method == '':
        allSchool = School.objects.all()
        return render(request, 'backEnd/showSchoolList.html', {'object': allSchool})

    else:
        return HttpResponse('没有该方法')


def topic(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addProvince':
        name = request.POST.get('topic_name')
        tag = request.POST.get('topic_tag')

        topic = Topic(
            t_name = name,
            t_click = 0,
            t_tag = tag,
        )
        topic.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/topic/show/')
    elif method == 'change':
        return render(request, 'backEnd/changeTopic.html', {'object': Topic.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            topic = {'t_name': request.POST.get('topic_name'),
                     't_tag': request.POST.get('topic_tag'),
                     'id': request.POST.get("id")
                     }
            Topic.objects.filter(id=topic['id']).update(t_name=topic['t_name'],t_tag=topic['t_tag'])

        return HttpResponseRedirect('/dc/topic/show')

    elif method == 'delete':
        Topic.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request, 'backEnd/addTopicView.html')
    elif method == 'show':
        # return HttpResponse("hello")
        return render(request, 'backEnd/showTopicList.html', {'object': Topic.objects.all()})
    else:
        return HttpResponse('没有该方法')


def feature(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')

    if method == 'addFeature':
        f_name = request.POST.get("f_name")
        f_topic = request.POST.get("f_topic")

        feature = Feature(
            f_name=f_name,
            f_topic=f_topic,
        )
        feature.save()

        return HttpResponseRedirect('/dc/feature/show')
    elif method == 'change':
        feature = Feature.objects.get(id=Oid)
        topics = Topic.objects.all()
        return render(request, 'backEnd/changeFeature.html', {'feature': feature, 'topics': topics})

    elif method == 'save':
        if request.method == 'POST':
            feature = {'f_name': request.POST.get('f_name'),
                       'f_topic': request.POST.get("f_topic"),
                       'id': request.POST.get("id"),
                       }

        Feature.objects.filter(id=feature['id']).update(f_name=feature['f_name'],
                                                        f_topic=feature['f_topic']
                                                        )

        return HttpResponseRedirect('/dc/feature/show/')

    elif method == 'delete':
        Feature.objects.filter(id=Oid).delete()

        return HttpResponseRedirect('../show')
    elif method == 'add':
        topics = Topic.objects.all()
        return render(request, 'backEnd/addFeatureView.html', {'topics': topics})
    elif method == 'show' or method == '':
        allFeature = Feature.objects.all()
        return render(request, 'backEnd/showFeatureList.html', {'object': allFeature})

    else:
        return HttpResponse('没有该方法')

def user(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addProvince':
        name = request.POST.get('topic_name')

        topic = Topic(
            t_name=name,
            t_click=0,
        )
        topic.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/topic/show/')
    elif method == 'change':
        host = Host.objects.get(id=Oid)
        features = host.get_all_features()
        host.features =  features.values()
        host.image = "/files/icons/"+host.icon.split("/")[-1]
        return render(request, 'backEnd/host-index.html', {'user': host})
    
    elif method == 'pass':
        

        Host.objects.filter(id=Oid).update(state=2)

        return HttpResponseRedirect('/dc/user/host/')

    elif method == 'delete':
        Topic.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'applying':
        users = Host.objects.filter(state=1)
        for each_host in users:
            each_host.userState = "<a href = '../pass/"+str(each_host.id)+"'>申请中(点击通过)</a>"
        
        return render(request, 'backEnd/showUserList.html', {'object':users})

    elif method == 'show':
        # return HttpResponse("hello")
        users = Host.objects.filter(state=0)
        for each_host in users:
            each_host.userState = "正常用户"
        return render(request, 'backEnd/showUserList.html', {'object':users})
    elif method == 'host':
        # return HttpResponse("hello")
        users = Host.objects.filter(state=2)
        for each_host in users:
            each_host.userState = "分享者"
        return render(request, 'backEnd/showUserList.html', {'object':users})
    else:
        return HttpResponse('没有该方法')


def test(request):
    '''
    find all provinces
    then get all university of each province.

    '''
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

    return render(request, "frontEnd/index.html", {"object": obj})


def s(request):
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


##################################################################################################
#  file operation 
#   about image and video
##################################################################################################

def addImage(request):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if request.method == "POST":
        return HttpResponse(1)
    return render(request, 'backEnd/addImage.html')


def addImageInfo(request):
    if request.method == "POST":
        des_origin_path = settings.UPLOAD_PATH + '/images/' + request.POST.get('title')
        des_origin_f = open(des_origin_path, "ab")
        tmpImg = request.FILES['img']
        for chunk in tmpImg.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()
        img = Image(
            title=request.POST.get('title'),
            location=des_origin_path,
            uploadUser=request.session['username'],
        )
        img.save()
        return HttpResponseRedirect('showImgList')
    return HttpResponse('allowed only via POST')


def showImgList(request):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    return render(request, 'backEnd/showImgList.html', {'image': Image.objects.all()})


def deleteImg(request, Oid):
    Image.objects.filter(id=Oid).delete()
    return HttpResponseRedirect('../showImgList')


##################################################################################################
#  email operation 
#   about check and inform 
##################################################################################################

def setEmail(request):

    #em = EmailMessage('subject','body','yhydhxson@126.com',['yhydhx@126.com'],['yhydhx@126.com'])
    subject,from_email,to = 'hello','yhydhxson@126.com','271086337@qq.com'
    text_content = 'This is an important message'
    html_content = u'<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content, 'text/html')
    
    # mail_list = ['yhydhx@126.com']
    # title = "this is a test"
    # context = "<a href='http://www.baidu.com'>helloworld</a>"
    # subject, from_email, to = title, EMAIL_HOST_USER, mail_list
    
    # html_content = context     
    # msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    # msg.attach_alternative(html_content, "text/html")
    
    msg.send()
    
    return HttpResponse("succuss")



