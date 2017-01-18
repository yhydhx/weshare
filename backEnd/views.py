# coding: utf-8  
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, RequestContext
from django.core.urlresolvers import reverse
from django.views import generic

from django import forms

# mail section
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context, loader

from gt.models import *
import datetime
from django.utils import timezone
from django.conf import settings
from gt.settings import *

from django.utils.http import urlquote

import hashlib,json
import datetime

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

def country(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addCountry':
        name = request.POST.get('country_name')
        c_id = request.POST.get('country_id')

        country = Country(
            c_name=name,
            c_id=int(c_id),
        )
        country.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/country/show/')
    elif method == 'change':
        return render(request, 'backEnd/changeCountry.html', {'object': Country.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            country = {'c_name': request.POST.get('country_name'),
                        'c_id': request.POST.get('country_id'),
                        'id': request.POST.get("id")
                        }
            Country.objects.filter(id=country['id']).update(c_name=country['c_name'], c_id=country['c_id'])

        return HttpResponseRedirect('/dc/country/show/')

    elif method == 'delete':
        Country.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')
    elif method == 'add':
        return render(request, 'backEnd/addCountryView.html')
    elif method == 'show':
        # return HttpResponse("hello")
        return render(request, 'backEnd/showCountryList.html', {'object': Country.objects.all()})
    else:
        return HttpResponse('没有该方法')




def province(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addProvince':
        name = request.POST.get('province_name')
        p_id = request.POST.get('province_id')
        c_name = request.POST.get("c_name")
        province = Province(
            p_name= name,
            p_id= int(p_id),
            p_country = c_name
        )

        province.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/province/show/')
    elif method == 'change':
        countries = Country.objects.all()
        return render(request, 'backEnd/changeProvince.html', {'object': Province.objects.get(id=Oid),'countries':countries})
    elif method == 'save':
        if request.method == 'POST':
            province = {'p_name': request.POST.get('province_name'),
                        'p_id': request.POST.get('province_id'),
                        'p_country': request.POST.get('c_name'),
                        'id': request.POST.get("id")
                        }
            Province.objects.filter(id=province['id']).update(p_name=province['p_name'], p_id=province['p_id'],p_country=province['p_country'])

        return HttpResponseRedirect('/dc/province/show/')

    elif method == 'delete':
        Province.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')
    elif method == 'add':
        countries = Country.objects.all()
        Info = {}
        Info['countries'] = countries
        return render(request, 'backEnd/addProvinceView.html',Info)
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

        return HttpResponseRedirect('/dc/school/show/')
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

        return HttpResponseRedirect('/dc/school/show/')

    elif method == 'delete':
        School.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')

    elif method == 'add':
        provinces = Province.objects.all()
        return render(request, 'backEnd/addSchoolView.html', {'provinces': provinces})
    elif method == 'show' or method == '':
        allSchool = School.objects.all()
        return render(request, 'backEnd/showSchoolList.html', {'object': allSchool})

    elif method == 'addImageView':
        school = School.objects.get(id=Oid)
        return render(request, 'backEnd/addSchoolImage.html', {'school': school})

    elif method == 'addImage':
        if request.method == "POST":
            mark_list = hashlib.new('md5', timezone.datetime.now().strftime("%Y-%m-%d %H:%I:%S")).hexdigest()
            des_origin_path = settings.UPLOAD_PATH + 'icons/' + mark_list + '.jpeg'  # mark_list是唯一的标志
            des_origin_f = open(des_origin_path, "ab")
            tmpImg = request.FILES['img']
            for chunk in tmpImg.chunks():
                des_origin_f.write(chunk)
            des_origin_f.close()
           
            School.objects.filter(id=Oid).update( s_image =  '/files/icons/' + mark_list + '.jpeg')

            return HttpResponseRedirect('/dc/school/show')
        else:
            return HttpResponse('allowed only via POST')

    elif method == 'generateJS':
        s = School()
        result = s.get_country_province_school()
        write_js(result)
        return HttpResponse(result)
        return render(request, 'backEnd/school/show/')
    else:
        return HttpResponse('没有该方法')

def write_js(result):
    output_file = file("gt/static/frontEnd/js/schoolsearch/allunivlist.js",'w')
    output_file.write('var allUnivList = ')
    output_file.write(json.dumps(result))

def topic(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addProvince':
        name = request.POST.get('topic_name')
        tag = request.POST.get('topic_tag')
        intro = request.POST.get("topic_intro")
        index = request.POST.get("topic_index")

        topic = Topic(
            t_name=name,
            t_click=0,
            t_tag=tag,
            t_index = index,
            t_intro = intro
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
                     't_intro': request.POST.get('topic_intro'),
                     't_index': request.POST.get('topic_index'),
                     'id': request.POST.get("id")
                     }
            Topic.objects.filter(id=topic['id']).update(t_name=topic['t_name'], t_tag=topic['t_tag'],t_intro=topic['t_intro'], t_index=topic['t_index'])

        return HttpResponseRedirect('/dc/topic/show/')

    elif method == 'delete':
        Topic.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')
    elif method == 'add':
        return render(request, 'backEnd/addTopicView.html')
    elif method == 'show':
        # return HttpResponse("hello")
        return render(request, 'backEnd/showTopicList.html', {'object': Topic.objects.all()})
    else:
        return HttpResponse('没有该方法')



def minortopic(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('/dc/login.html')

    if method == 'addMinorTopic':

        m_name = request.POST.get("m_name")
        m_topic = request.POST.get("m_topic")
        m_index = request.POST.get("m_index")
        m_introduction = request.POST.get("m_introduction")


        minortopic = Minor_Topic(
            m_name = m_name ,
            m_topic = m_topic ,
            m_index = m_index ,
            m_introduction = m_introduction ,
        )
        minortopic.save()

        return HttpResponseRedirect('/dc/minortopic/show/')
    elif method == 'change':
        minor = Minor_Topic.objects.get(id=Oid)
        topics = Topic.objects.all()
        return render(request, 'backEnd/changeMinorTopic.html', {'minor': minor, 'topics': topics})

    elif method == 'save':
        if request.method == 'POST':
            minor = {   'id' : request.POST.get('id'),
                       "m_name" : request.POST.get("m_name"),
                        "m_topic":  request.POST.get("m_topic"),
                        "m_index" : request.POST.get("m_index"),
                        "m_introduction" : request.POST.get("m_introduction"),
                       }

        Minor_Topic.objects.filter(id=minor['id']).update(
                                                        m_name = minor['m_name'],
                                                        m_topic = minor['m_topic'],
                                                        m_index = minor['m_index'],
                                                        m_introduction = minor['m_introduction'],
                                                        )

        return HttpResponseRedirect('/dc/minortopic/show/')

    elif method == 'delete':
        Minor_Topic.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')
    elif method == 'add':
        topics = Topic.objects.all()
        return render(request, 'backEnd/addMinorTopicView.html', {'topics': topics})
    elif method == 'show' or method == '':
        allMinorTopic = Minor_Topic.objects.all()
        return render(request, 'backEnd/showMinorTopicList.html', {'object': allMinorTopic})

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

        return HttpResponseRedirect('/dc/feature/show/')
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

        return HttpResponseRedirect('../show/')
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
        f = Feature()
        questions = f.get_one_host_questions(Oid)
        host = Host.objects.get(id=Oid)
        Info = {}
        Info['host'] = host.format_dict_with_school_name()
        Info['msgs'] = host.get_user_message(host.id)
        Info['questions'] = questions
        Info['certification'] = host.get_one_host_passed_certification(host)

        return render(request, 'backEnd/host-index-dc.html', Info)

    elif method == 'pass':

        #send email 
        host = Host.objects.get(id=Oid)
        admin_id = request.session['adminname']
        subject = "恭喜您成功成为我们的HOST!"
        content = "恭喜您成为我们的分享者！"
        to = [host.email]

        #to = ["yhydhx@126.com"]
        mail = Mail()
        mail.host_pass(to,content,host,admin_id)

        Host.objects.filter(id=Oid).update(state=2)


        return HttpResponseRedirect('/dc/user/host/')

    elif method == "degrade":
        host = Host.objects.get(id=Oid)
        host.state = HOST_STATE['APPLY']
        host.save()
        return HttpResponseRedirect("/dc/user/host/")

    elif method == 'delete':
        Host.objects.filter(id=Oid).delete()
        Host_Topic.objects.filter(host_id = Oid).delete()
        Message.objects.filter(from_user=Oid).delete()

        return HttpResponseRedirect('../show/')
    elif method == 'applying':
        users = Host.objects.filter(state=1)
        for each_host in users:
            each_host.userState = "<a href = '../pass/" + str(each_host.id) + "'>申请中(点击通过)</a>"

        return render(request, 'backEnd/showUserList.html', {'object': users})

    elif method == 'show':
        # return HttpResponse("hello")
        users = Host.objects.filter(state=0)
        for each_host in users:
            each_host.userState = "正常用户"
        return render(request, 'backEnd/showUserList.html', {'object': users})
    elif method == 'host':
        # return HttpResponse("hello")
        users = Host.objects.filter(state=2)
        for each_host in users:
            each_host.userState = "分享者"
        return render(request, 'backEnd/showHostList.html', {'object': users})
    elif method == 'mail':
        host = Host.objects.get(id=Oid)
        return render(request, 'backEnd/sendMail.html',{'object':host})
    elif method == 'sendMail':
        host = Host.objects.get(id=Oid)
        subject = request.POST.get('subject')
        content = request.POST.get('mail_text')
        to = [host.email]
        # sendMail(subject,to,content)

        mail = Mail(
            subject = subject,
            from_email = EMAIL_HOST_USER,
            to_email = host.email,
            host_id = host.id,
            admin_id = request.session['adminname'],
            content = content,
            is_success = 0
            )
        mail.save()
        mail.sendMail(subject,to,content)
        #send success, update the data
        mail.is_success = 1
        mail.save()

        return HttpResponseRedirect("../show/")
    else:
        return HttpResponse('没有该方法')

# def sendMail(subject,to,content):
#     #to = ['yhydhx@126.com']

#     context = {"content": content,
#                "link": "http://wshere.com/identify/kaixun/jdklafwioejfioqw",
#                }
#     email_template_name = 'backEnd/blankTemp.html'
#     t = loader.get_template(email_template_name)

#     from_email = EMAIL_HOST_USER

#     html_content = t.render(Context(context))
#     #print html_content
#     msg = EmailMultiAlternatives(subject, html_content, from_email, to)
#     msg.attach_alternative(html_content, "text/html")

#     msg.send()


def menu(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')
    if method == 'addMenu':
        name = request.POST.get('menu_name')
        index = request.POST.get('menu_index')

        menu = Menu(
            m_name = name,
            m_index = index,
            m_upload_time = datetime.datetime.now()
        )
        menu.save()
        # Oid = news.id
        return HttpResponseRedirect('/dc/menu/show/')
    elif method == 'change':
        return render(request, 'backEnd/changeMenu.html', {'object': Menu.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            menu = {'m_name': request.POST.get('menu_name'),
                     'm_index': request.POST.get('menu_index'),
                     'id': request.POST.get("id")
                     }

            print menu         
            Menu.objects.filter(id=menu['id']).update(m_name=menu['m_name'],m_index=menu['m_index'])

        return HttpResponseRedirect('/dc/menu/show/')

    elif method == 'delete':
        Menu.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show/')
    elif method == 'add':
        return render(request, 'backEnd/addMenuView.html')
    elif method == 'show':
        # return HttpResponse("hello")
        return render(request, 'backEnd/showMenuList.html', {'object': Menu.objects.all()})
    else:
        return HttpResponse('没有该方法')




def doc(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')

    if method == 'addDoc':
        d_name = request.POST.get("d_name")
        d_menu = request.POST.get("d_menu")
        d_text = request.POST.get("d_text")
        d_index = request.POST.get("d_index")


        doc = Document(
            d_name = d_name,
            d_menu = d_menu,
            d_text = d_text,
            d_index = d_index
        )
        doc.save()

        return HttpResponseRedirect('/dc/doc/show/')
    elif method == 'change':
        doc = Document.objects.get(id=Oid)
        menu = Menu.objects.all()
        return render(request, 'backEnd/changeDoc.html', {'doc': doc, 'menu': menu})

    elif method == 'save':
        if request.method == 'POST':
            doc = {'d_name': request.POST.get('d_name'),
                    'd_text': request.POST.get("d_text"),
                    'd_menu': request.POST.get("d_menu"),
                    'd_index': request.POST.get("d_index"),
                       'id': request.POST.get("id"),
                       }

        Document.objects.filter(id=doc['id']).update(d_name=doc['d_name'],
                                                        d_text=doc['d_text'],
                                                        d_index=doc['d_index'],
                                                        d_menu=doc['d_menu']
                                                        )

        return HttpResponseRedirect('/dc/doc/show/')

    elif method == 'delete':
        Document.objects.filter(id=Oid).delete()

        return HttpResponseRedirect('../show/')
    elif method == 'add':
        menu = Menu.objects.all()
        return render(request, 'backEnd/addDocView.html', {'menu': menu})
    elif method == 'show' or method == '':
        allFeature = Document.objects.all()
        for doc_atom in allFeature:
            doc_atom.format_menu()
        return render(request, 'backEnd/showDocList.html', {'object': allFeature})

    else:
        return HttpResponse('没有该方法')

def test(request):

    return render(request, "backEnd/test.html")

def getUserNameList(request):
    username = request.GET.get("userName")
    schoolID = request.GET.get("schoolID")
    hosts = Host.objects.filter(state=HOST_STATE['HOST'])

    response_data = []
    for host_atom in hosts:
        if not schoolID in [host_atom.bachelor , host_atom.graduate , host_atom.phd]:
            continue

        #print host_atom.username, username , host_atom.username.startswith(username)
        if host_atom.username.startswith(username):
            tmpD = {}
            tmpD['userName'] = host_atom.username
            tmpD['id'] = host_atom.id
            response_data.append(tmpD)

    return HttpResponse(json.dumps(response_data))



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
            print each_host.username, d_topic_detail[t_id]['name']
        # complete tags
        for k, v in d_host_topic.items():
            tag = tag + " " + v

        each_host.image = "/files/icons/" + each_host.icon.split("/")[-1]
        each_host.min_payment = int(each_host.min_payment)
        each_host.tag = tag

    Info = {}
    Info['object'] = hosts
    Info['topics'] = d_topic_detail.values()

    Info['allPeople'] = len(hosts)

    return render(request, "frontEnd/school.html", Info)





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
    # em = EmailMessage('subject','body','service@wshere  .com',['yhydhx@126.com'],['yhydhx@126.com'])
    # em.send()

    # subject,from_email,to = 'hello','service@wshere.com','271086337@qq.com'
    # text_content = 'This is an important message'
    # html_content = u'<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
    # msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()

    mail_list = ['yhydhx@126.com']
    title = "this is a test"
    context = {"context": "<a href='http://wshere.com/kaixuan'>helloworld</a>",
               "link": "http://wshere.com/identify/kaixun/jdklafwioejfioqw",
               }
    email_template_name = 'frontEnd/template.html'
    t = loader.get_template(email_template_name)

    subject, from_email, to = title, EMAIL_HOST_USER, mail_list

    html_content = t.render(Context(context))
    print html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    return HttpResponse("succuss")

#功能模块

def func(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')


    if method == 'generate_index_data':
        recommend_host = Host()
        Info = {}
        Info = recommend_host.get_index_all_classes()
        Info.update(recommend_host.get_index_statistic())

        try:
            cache = Cache.objects.get(cache_name = "index_data")
        except:
            cache = Cache(cache_name = "index_data")
        cache_content = str(Info)
        cache.cache_value = cache_content
        cache.cache_modify_time = datetime.datetime.now()
        cache.save()
        return HttpResponse(json.dumps(Info), content_type="application/json")
        return HttpResponse('主页信息生成成功')
    elif method == 'compute_user_score':
        menu = Menu.objects.all()
        return render(request, 'backEnd/addDocView.html', {'menu': menu})
    elif method == 'show' or method == '':
        allFeature = Document.objects.all()
        for doc_atom in allFeature:
            doc_atom.format_menu()
        return render(request, 'backEnd/showDocList.html', {'object': allFeature})

    else:
        return HttpResponse('没有该方法')

def certification(request, method, Oid):
    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')

    if method == 'passed':
        crt = Certificate.objects.filter(c_state = CERTIFICATE_STATE['PASSED'])
        return render(request, 'backEnd/showCertificationList.html', {'menu': menu})

    elif method  == "passing":
        if request.method == "POST":
            c_id = request.POST.get("id")
            crt = Certificate.objects.get(id = c_id)
            crt.c_state = CERTIFICATE_STATE['PASSED']
            crt.save()
            return HttpResponseRedirect("/dc/certification/show")

    elif method == "failed":
        crt = Certificate.objects.filter(c_state = CERTIFICATE_STATE['FAILED'])
        return render(request, 'backEnd/showCertificationList.html', {'menu': menu})
    elif method == 'show' or method == '':
        crt = Certificate.objects.filter(c_state = CERTIFICATE_STATE['CERTIFYING'])
        crt_list = []
        for crt_atom in crt: 
            crt_list.append(crt_atom.format_dict())
        return render(request, 'backEnd/showCertificationList.html', {'object': crt_list})
    elif method == "change":
        crt = Certificate.objects.get(id = Oid)
        return render(request, 'backEnd/changeCertification.html', {'object': crt})
    else:
        return HttpResponse('没有该方法')

def appointment(request, method, Oid):
    '''
    'INITED': 0,  # 创建订单
    'CERTIFIED': 1,  # 确认
    'PAID': 2,  # 付款
    'COMPLETED': 3,  # 完成了
    'FINISHED': 4  # 结算完成
    '''

    try:
        request.session['adminname']
    except KeyError, e:
        return HttpResponseRedirect('login.html')

    if method == 'inited':
        obj = []
        appt = Appointment.objects.filter(state = APPOINTMENT_STATE['INITED'])
        for app in appt: obj.append(app.format_dict_on_manage())
        return render(request, 'backEnd/showAppointmentList.html', {'object': obj})
    
    elif method == "certified":
        obj = []
        appt = Appointment.objects.filter(state = APPOINTMENT_STATE['CERTIFIED'])
        for app in appt: obj.append(app.format_dict_on_manage())
        return render(request, 'backEnd/showAppointmentList.html', {'object': obj})
    
    elif method == "paid":
        obj = []
        appt = Appointment.objects.filter(state = APPOINTMENT_STATE['PAID'])
        for app in appt: obj.append(app.format_dict_on_manage())
        return render(request, 'backEnd/showAppointmentList.html', {'object': obj})
    
    elif method == "complete":
        obj = []
        appt = Appointment.objects.filter(state = APPOINTMENT_STATE['COMPLETED'])
        for app in appt: obj.append(app.format_dict_on_manage())
        return render(request, 'backEnd/showAppointmentList.html', {'object': obj})
    
    elif method == "finished":
        obj = []
        appt = Appointment.objects.filter(state = APPOINTMENT_STATE['FINISHED'])
        for app in appt: obj.append(app.format_dict_on_manage())
        return render(request, 'backEnd/showAppointmentList.html', {'object': obj})
    

    # elif method  == "passing":
    #     if request.method == "POST":
    #         c_id = request.POST.get("id")
    #         crt = Certificate.objects.get(id = c_id)
    #         crt.state = APPOINTMENT_STATE['PASSED']
    #         crt.save()
    #         return HttpResponseRedirect("/dc/certification/show")

    # elif method == "failed":
    #     crt = Certificate.objects.filter(state = APPOINTMENT_STATE['FAILED'])
    #     return render(request, 'backEnd/showCertificationList.html', {'menu': menu})
    # elif method == 'show' or method == '':
    #     crt = Certificate.objects.filter(state = APPOINTMENT_STATE['CERTIFYING'])
    #     crt_list = []
    #     for crt_atom in crt: 
    #         crt_list.append(crt_atom.format_dict())
    #     return render(request, 'backEnd/showCertificationList.html', {'object': crt_list})
    # elif method == "change":
    #     crt = Certificate.objects.get(id = Oid)
    #     return render(request, 'backEnd/changeCertification.html', {'object': crt})
    else:
        return HttpResponse('没有该方法')

