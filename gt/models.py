# coding:utf-8

from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField
from django import forms
from settings import EMAIL_HOST_USER
from django.shortcuts import render
from django.template import Context

# mail server
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context, loader
from gt.settings import *


import hashlib,binascii,datetime,random


class Host(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    register_time = models.DateTimeField(null=True)
    # 以上为必选信息
    gender = models.IntegerField(default=1, blank=True)  # 1是男生 0是女生
    motto = models.CharField(max_length=100, blank=True)
    introduction = models.CharField(max_length=2000, blank=True)
    icon = models.CharField(max_length=200)
    orders = models.IntegerField(default=0)
    service_time = models.CharField(max_length=100, default=True)
    max_payment = models.FloatField(default=0)
    min_payment = models.FloatField(default=0)
    
    state = models.IntegerField(default=0)  # normal user  => 0  examing => 1  sharer => 2

    birth = models.CharField(blank=True, max_length=100)
    qq_number = models.CharField(blank=True, max_length=20)
    wechat = models.CharField(blank=True, max_length=20)
    h_school = models.CharField(max_length=200)

    #Education Infomation
    education = models.IntegerField(default=0)  # bachlor => 0  graduate => 1 phd => 2 else => 3
    bachelor = models.CharField(blank=True, max_length=100)
    graduate = models.CharField(blank=True, max_length=100)
    phd = models.CharField(blank=True, max_length=100)

    bachelor_major = models.CharField(blank=True, max_length=100)
    graduate_major = models.CharField(blank=True, max_length=100)
    phd_major = models.CharField(blank=True, max_length=100)

    #  qq_login information::
    open_id = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.username

    def general_search(self,word_1,word_2):
        '''
        a).   “分享家”的一句话简介；
        b).   学校&专业；
        c).   咨询服务列表（“分享家”自定义输入的具体内容）；
        d).   前述咨询服务列表所涉及到的大话题&小话题；
        e).   详细的自我介绍；
        f).    线上问答的数据（如果有线上问答&且线上问答有文字数据记录的话，例如：分答的提问是文字形式，回答只有语音，则只需要从提问的问题中检索关键字）；
        g).   “提问者”在完成订单后的文字评价（如果技术上复杂，则可以免去这个部分的信息）；
        '''
        all_host = Host.objects.all()
        result = []

        for host_atom in all_host:
            search_string = ""
            search_string += host_atom.username+" "
            search_string += host_atom.motto+" "
            education = host_atom.education
            #get the school infomation
            if education == 0:
                try:
                    bachelor_school = School.objects.get(s_name = host_atom.bachelor).s_name
                    search_string += bachelor_school + " "
                except :
                    pass
            elif education == 1:
                try:
                    graduate_school = School.objects.get(s_name = host_atom.graduate).s_name
                    search_string += graduate + " "
                    bachelor_school = School.objects.get(s_name = host_atom.bachelor).s_name
                    search_string += bachelor_school + " "
                except:
                    pass
            elif education == 2:
                try:
                    graduate_school = School.objects.get(s_name = host_atom.graduate).s_name
                    search_string += graduate + " "
                    bachelor_school = School.objects.get(s_name = host_atom.bachelor).s_name
                    search_string += bachelor_school + " "
                    phd_school = School.objects.get(s_name = host_atom.phd).s_name
                    search_string += phd_school + " "
                except:
                    pass
            #服务列表
            
            topic_hosts = Host_Topic.objects.filter(host_id = host_atom.id)
            topic_list = {}
            minor_topic_list = {}
            feature_list = {}
            for topic_host_atom in topic_hosts:
                t_id = topic_host_atom.t_id
                m_id = topic_host_atom.m_id
                f_id = topic_host_atom.f_id

                topic_list[t_id] = 1
                minor_topic_list[m_id] = 1
                feature_list[f_id] = 1

            # add topic 
            for topic_atom in topic_list:
                topic = Topic.objects.get(id=topic_atom)
                search_string += topic.t_name + " "


            for minor_atom in minor_topic_list:
                minor = Minor_Topic.objects.get(id=minor_atom)
                search_string += minor.m_name + " "

            for feature_atom in feature_list:
                feature = Feature.objects.get(id=feature_atom)
                search_string += feature.f_name + " "
            

            #introduction 
            search_string += host_atom.introduction + " "

            #etc
            #

            if word_1 in search_string and word_2 in search_string:
                result.append(host_atom.format_dict())

        return result





    def encode_password(self,s):
        return hashlib.md5(s).hexdigest()

    def format_dict(self):
        tmpHost = {}
        tmpHost["username"] =  self.username
        tmpHost["gender"] =  self.gender
        tmpHost["motto"] =  self.motto
        tmpHost["introduction"] =  self.introduction
        tmpHost["icon"] =  self.icon
        tmpHost["orders"] =  self.orders
        tmpHost["service_time"] =  self.service_time
        tmpHost["max_payment"] =  self.max_payment
        tmpHost["min_payment"] =  self.min_payment
        
        tmpHost["state"] =  self.state

        tmpHost["birth"] =  self.birth
        tmpHost["qq_number"] =  self.qq_number
        tmpHost["wechat"] =  self.wechat

        #Education Infomation
        tmpHost["education"] =  self.education
        tmpHost["bachelor"] =  self.bachelor
        tmpHost["graduate"] =  self.graduate
        tmpHost["phd"] =  self.phd

        try:
            tmpHost['id'] = self.id
        except:
            pass
        return tmpHost

    def get_all_features(self):
        host_topics = Host_Topic.objects.filter(host_id=self.id)
        d_topic_feature = {}
        for single_feature in host_topics:
            t_id = single_feature.t_id
            f_id = single_feature.f_id

            if not d_topic_feature.has_key(t_id):
                d_topic_feature[t_id] = {}
                d_topic_feature[t_id]['name'] = Topic.objects.get(id=t_id).t_name
                d_topic_feature[t_id]['features'] = []
                d_topic_feature[t_id]['row1'] = []
                d_topic_feature[t_id]['row2'] = []
                d_topic_feature[t_id]['row3'] = []
                d_topic_feature[t_id]['row4'] = []

            d_topic_feature[t_id]['features'].append(Feature.objects.get(id=f_id).f_name)

        for t_id, value in d_topic_feature.items():
            count = 0
            for f in d_topic_feature[t_id]['features']:
                count += 1
                if count % 4 == 1:
                    d_topic_feature[t_id]['row1'].append(f)
                elif count % 4 == 2:
                    d_topic_feature[t_id]['row2'].append(f)
                elif count % 4 == 3:
                    d_topic_feature[t_id]['row3'].append(f)
                elif count % 4 == 0:
                    d_topic_feature[t_id]['row4'].append(f)

        return d_topic_feature


    def get_all_classes(self, school_id="none"):
        hosts=[]
        if school_id == "none":
            hosts = Host.objects.filter(state=2)
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
                    print t_id
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
                #print each_host.username, d_topic_detail[t_id]['name']
            # complete tags
            for k, v in d_host_topic.items():
                tag = tag + " " + str(v)

            each_host.image = "/files/icons/" + each_host.icon.split("/")[-1]
            each_host.min_payment = int(each_host.min_payment)
            each_host.tag = tag



        Info = {}
        Info['hosts'] = []

        for host_atom in hosts:
            tmpHost = host_atom.format_dict()
            Info['hosts'].append(tmpHost)

        Info['topics'] = d_topic_detail.values()
        #print Info['topics']
        return Info

    def get_user_message(self,user_id):
        msgs = Message.objects.filter(to_user=user_id)
        msg_result = []
        for msg_atom in msgs:
            tmp_message = {}
            tmp_message = msg_atom.format_dict()
            tmp_message['name'] = Host.objects.get(id=msg_atom.from_user).username
            msg_result.append(tmp_message)
        return msg_result

    def get_index_statistic(self):
        '''
        get guests'number and hosts' number 
        And schools' number
        '''
        Info = {}
        Info['register_num'] = 0
        Info['host_num'] = 0
        Info['normal_num'] = 0
        hosts = Host.objects.all()
        univ = {}
        for host_atom in hosts:
            Info['register_num'] += 1
            if host_atom.state == 2:
                Info['host_num'] += 1
            elif host_atom.state == 1 or host_atom.state == 0:
                Info['normal_num'] += 1

            #Get the School Infomation 
            if not univ.has_key(host_atom.h_school):
                univ[host_atom.h_school] = 1
            else:
                univ[host_atom.h_school] += 1

        Info['school_num'] = len(univ)

        return Info

    def get_index_schools(self):
        '''
            show top schools on index 
        '''
        schools = School.objects.all().order_by('s_student_number')[:6]
        result = []
        for school_atom in schools:
            result.append(school_atom.format_dict())
        return result

    def search_user_with_key(self,keyword):
        result_hosts = []
        all_hosts = Host.objects.all()
        
        for host_atom in all_hosts:
            #first step : search the name
            if keyword in host_atom.username:
                result_hosts.append(host_atom)
            #second step : search the introduction
            if keyword in host_atom.introduction:
                result_hosts.append(host_atom)
            #third type , search the motto
            if keyword in host_atom.motto:
                result_hosts.append(host_atom)

        return result_hosts

    def get_one_user_host_bills(self):
        bills = Appointment.objects.filter(from_user_id = self.id)

        result = []
        for bill_atom in bills:
            tmp_bill = bill_atom.format_dict_on_manage()
            result.append(tmp_bill)

        return result

    def get_one_host_user_bills(self):
        bills = Appointment.objects.filter(to_host_id = self.id)
        result = []
        for bill_atom in bills:
            tmp_bill = bill_atom.format_dict_on_manage()
            result.append(tmp_bill)
        return result

class Country(models.Model):
    c_name = models.CharField(max_length=100)
    c_id = models.IntegerField()

class Province(models.Model):
    p_country = models.CharField(max_length=100, null=True)
    p_name = models.CharField(max_length=100)
    p_id = models.IntegerField()


class School(models.Model):
    s_name = models.CharField(max_length=200)
    s_province = models.CharField(max_length=200)
    s_display_index = models.IntegerField()
    s_student_number = models.IntegerField()
    s_image = models.CharField(max_length=100,null=True)
    
    def format_dict(self):
        tmp_school = {}
        tmp_school['s_name'] = self.s_name
        tmp_school['s_province'] = self.s_province
        tmp_school['s_display_index'] = self.s_display_index
        tmp_school['s_student_number'] = self.s_student_number
        tmp_school['s_image'] = self.s_image
        return tmp_school

    def get_single_school_detail(self,school_id):
        self.school_union = {}
        host_bachelor  = Host.objects.filter(state=2, bachelor=school_id)
        host_graduate  = Host.objects.filter(state=2, graduate=school_id)
        host_phd  = Host.objects.filter(state=2, phd=school_id)



        self.d_topic_detail = {}
        for each_host in host_bachelor:
            self.format_user_in_school(each_host)
        for each_host in host_graduate:
            self.format_user_in_school(each_host)
        for each_host in host_phd:
            self.format_user_in_school(each_host)

        return self.school_union.values(),self.d_topic_detail.values()

    
    def format_user_in_school(self,each_host):
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
        d_topic_detail = self.d_topic_detail
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
                d_topic_detail[t_id]['hosts'] = {}

            d_topic_detail[t_id]['hosts'][each_host.id] = 1
            d_topic_detail[t_id]['number'] = len(d_topic_detail[t_id]['hosts'])
            d_host_topic[t_id] = d_topic_detail[t_id]['tag']

            # print d_topic_detail[t_id]['topics']
            # print d_topic_detail[t_id]
            # print each_host.username, d_topic_detail[t_id]['name']
        # complete tags

        for k, v in d_host_topic.items():
            tag = tag + " " + str(v)

        tmp_host = Host.format_dict(each_host)
        tmp_host['image'] =  "/files/icons/" + each_host.icon.split("/")[-1]
        tmp_host['min_payment'] = int(each_host.min_payment)
        tmp_host['tag'] =  tag

        self.school_union[each_host.id] = tmp_host

        self.d_topic_detail = d_topic_detail

    def get_country_province_school(self):
        result = []
        countries = Country.objects.all()

        # get each country 
        country_index = 0
        for country in countries:
            tmpC = {}
            tmpC['id'] = country_index
            tmpC['univs'] = ""
            tmpC['name'] = country.c_name
            tmpC['provs'] = []
            country_index += 1
            #get each province 
            
            provinces = Province.objects.filter(p_country = country.c_name)
            province_index = 1
            for province in provinces:
                tmpP = {}
                tmpP['country_id'] = tmpC['id']
                tmpP['id'] = province_index
                tmpP['name'] = province.p_name
                tmpP['univs'] = []
                province_index += 1

                #get each school 
                schools  = School.objects.filter(s_province=tmpP['name'], s_display_index = 1)
                school_index = 1
                for school in schools:
                    tmpS = {}
                    tmpS['id'] = tmpP['id'] * 1000 + school_index
                    tmpS['name'] = school.s_name
                    tmpS['school_id'] = school.id
                    school_index += 1
                    tmpP['univs'].append(tmpS)

                tmpC['provs'].append(tmpP)

            result.append(tmpC)
        return result

class Topic(models.Model):
    t_name = models.CharField(max_length=200)
    t_click = models.IntegerField(default=0)
    t_intro = models.CharField(max_length=200, null=True)
    t_tag = models.CharField(max_length=100, null=True)
    t_index = models.IntegerField(null=True)

    def get_minor_topic_of_one_topic(self,topic_name):
        result = []
        minor_topics = Minor_Topic.objects.filter(m_topic=topic_name)
        for minor_topic_atom in minor_topics:
            result.append(minor_topic_atom.format_dict())
        return result



class Minor_Topic(models.Model):
    m_name = models.CharField(max_length=100)
    m_click = models.IntegerField(default=0)
    m_topic = models.CharField(max_length=100)
    m_index = models.IntegerField(default=0)
    m_introduction = models.CharField(max_length=100)
    def format_dict(self):
        tmp_dict = {}
        tmp_dict['m_name'] = self.m_name
        tmp_dict['m_click'] = self.m_click
        tmp_dict['m_topic'] = self.m_topic
        tmp_dict['m_index'] = self.m_index
        tmp_dict['m_introduction'] = self.m_introduction
        tmp_dict['id'] = self.id
        return tmp_dict

class Feature(models.Model):
    f_name = models.CharField(max_length=200)
    f_topic = models.CharField(max_length=100)

    def get_one_user_features(self, user_id):
        h_topics = Host_Topic.objects.filter(host_id=user_id)

        # classification
        d_topic_feature = {}
        for h_topic_atom in h_topics:
            t_id = h_topic_atom.t_id
            f_id = h_topic_atom.f_id
            m_id = h_topic_atom.m_id

            #check the topic_id
            if not d_topic_feature.has_key(t_id):
                d_topic_feature[t_id] = {}
                d_topic_feature[t_id]['feature_list'] = []
                d_topic_feature[t_id]['intro'] = ""
            
            feature_atom = {}
            feature_atom['f_id'] = f_id
            feature_atom['m_id'] = m_id
            feature_atom['t_id'] = t_id
            d_topic_feature[t_id]['feature_list'].append(feature_atom)



        # transform the id into chinese
        result = []
        d_topic_feature_translate = {}
        for k, v in d_topic_feature.items():
            tmp_topic = Topic.objects.get(id=k)
            topic_name = tmp_topic.t_name
            topic_intro = tmp_topic.t_intro
            topic_id = tmp_topic.id
            topic_tag = tmp_topic.t_tag
            d_topic_feature_translate[topic_name] = {}
            d_topic_feature_translate[topic_name]['intro'] = topic_intro
            d_topic_feature_translate[topic_name]['name'] = topic_name
            d_topic_feature_translate[topic_name]['id'] = topic_id
            d_topic_feature_translate[topic_name]['tag'] = topic_tag
            d_topic_feature_translate[topic_name]['feature_list'] = []
            d_topic_feature_translate[topic_name]['minor_topic_list'] = tmp_topic.get_minor_topic_of_one_topic(topic_name)

            #get all minor topics 
            #
            
            #get all feature
            for feature_atom in v['feature_list']:
                tmp_feature = {}
                feature_single  = Feature.objects.get(id=feature_atom['f_id'])
                minor_singel = Minor_Topic.objects.get(id=feature_atom['m_id'])
                tmp_feature['f_name'] = feature_single.f_name
                tmp_feature['m_name'] = minor_singel.m_name
                tmp_feature['f_id'] = feature_single.id
                tmp_feature['m_id'] = minor_singel.id

                d_topic_feature_translate[topic_name]['feature_list'].append(tmp_feature)
        return  d_topic_feature_translate

    def get_one_user_features_with_all_topic(self, user_id):
        #COMPLETE THE BLANK MINOR TOPIC
        d_topic_feature_translate = self.get_one_user_features(user_id)
        topics = Topic.objects.all().order_by('t_index')
        result = []
        for topic_atom in topics:
            if not d_topic_feature_translate.has_key(topic_atom.t_name):
                tmp_dic = {}
                tmp_dic['intro'] = topic_atom.t_intro
                tmp_dic['name'] = topic_atom.t_name
                tmp_dic['id'] = topic_atom.id
                tmp_dic['feature_list'] = []
                tmp_dic['minor_topic_list'] = topic_atom.get_minor_topic_of_one_topic(topic_atom.t_name)
                result.append(tmp_dic)
            else:
                result.append(d_topic_feature_translate[topic_atom.t_name])
        return result

    def get_one_host_questions(self,user_id):
        h_topics = Host_Topic.objects.filter(host_id=user_id)

        # classification
        d_feature = {}
        for h_topic_atom in h_topics:
            f_id = h_topic_atom.f_id
            m_id = h_topic_atom.m_id
            t_id = h_topic_atom.t_id
            d_feature[f_id] = {}
            d_feature[f_id]['m_id'] = m_id
            d_feature[f_id]['t_id'] = t_id



        for feature_atom in d_feature:
            feature = Feature.objects.get(id=feature_atom)
            d_feature[feature_atom]['feature_name'] = feature.f_name
            d_feature[feature_atom]['feature_id'] = feature.id

        return d_feature.values()


class Host_Topic(models.Model):
    host_id = models.CharField(max_length=100)
    t_id = models.CharField(max_length=100)
    m_id = models.CharField(max_length=100)  #minor topic
    f_id = models.CharField(max_length=100)  # 关系库


class User_data(models.Model):
    host_id = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=100)


class Certificate(models.Model):  # igno
    host_id = models.CharField(max_length=100)
    c_name = models.CharField(max_length=200)
    c_state = models.IntegerField()


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Menu(models.Model):
    m_name = models.CharField(max_length=100)
    m_index = models.IntegerField()
    m_upload_time = models.DateTimeField(null=True)


class Document(models.Model):
    d_menu = models.CharField(max_length=100)
    d_name = models.CharField(max_length=100)
    d_text = models.TextField()
    d_index = models.IntegerField()  # 将不同的话题区分开来
    def format_menu(self):
        self.d_menu = Menu.objects.get(id=self.d_menu).m_name


class Forget(models.Model):
    user_id = models.CharField(max_length=200)
    forget_string = models.CharField(max_length=200)
    timestamp = models.DateTimeField()

    def _add_time(self):
        self.timestamp = timezone.datetime.now()


class Mail(models.Model):
    subject = models.CharField(max_length=200)
    from_email = models.CharField(max_length=200)
    to_email = models.CharField(max_length=200)
    host_id = models.CharField(max_length=200)
    admin_id = models.CharField(max_length=200)
    content = models.TextField()
    is_success = models.IntegerField()




    def sendMail(self, subject, to, content):
        # to = ['yhydhx@126.com']

        context = {"content": content}

        email_template_name = 'backEnd/blankTemp.html'
        t = loader.get_template(email_template_name)

        from_email = EMAIL_HOST_USER

        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    def register_success(self,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/register_success_template.html'
        t = loader.get_template(email_template_name)

        from_email = EMAIL_HOST_USER

        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    def host_pass(self,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/host_pass_template.html'
        t = loader.get_template(email_template_name)
        from_email = EMAIL_HOST_USER
        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def bill_info(self,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/bill_info_template.html'
        t = loader.get_template(email_template_name)
        from_email = EMAIL_HOST_USER
        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def report(self,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/report_template.html'
        t = loader.get_template(email_template_name)
        from_email = EMAIL_HOST_USER
        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def recruit(self,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/recruit_template.html'
        t = loader.get_template(email_template_name)
        from_email = EMAIL_HOST_USER
        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def forgotPassword(self, subject, to, content):
        context = {"content": content}

        email_template_name = 'backEnd/forget_password_template.html'
        t = loader.get_template(email_template_name)

        from_email = EMAIL_HOST_USER

        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        msg.send()




class Message(models.Model):
    from_user = models.CharField(max_length=100)
    to_user = models.CharField(max_length=100)
    message_type = models.IntegerField()
    icon = models.CharField(max_length=100)
    upload_time = models.DateTimeField()
    content = models.TextField()
    extra_id = models.CharField(max_length = 100, null = True)

    def date_format(self):
        self.upload_time = self.upload_time.strftime("%Y-%m-%d")

    def format_dict(self):
        self.date_format()
        tmp_message = {}
        tmp_message['from_user'] = self.from_user
        tmp_message['to_user'] = self.to_user
        tmp_message['message_type'] = self.message_type
        tmp_message['icon'] = self.icon
        tmp_message['upload_time'] = self.upload_time
        tmp_message['content'] = self.content

        try:
            tmp_message['id'] = self.id
        except:
            pass
            
        return tmp_message


class Bill(models.Model):
    bill_id = models.CharField(max_length = 100)        # 请与贵网站订单系统中的唯一订单号匹配  
    subject = models.CharField(max_length = 100)       # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。  
    body = models.CharField(max_length = 200)          # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空  
    bank = models.CharField(max_length = 200, default='alipay')
    total_fee = models.FloatField()                    
    create_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    state =  models.IntegerField()
    from_user_id = models.CharField(max_length = 100)
    to_host_id = models.CharField(max_length = 100)
    bill_type = models.IntegerField()



class Appointment(models.Model):
    '''
    这个来创建预约的步骤和环境，
    第一步：简要介绍自己的信息和想要咨询的问题，并告诉Host你想见面的时间和时长
    第二步：
    '''
    state = models.IntegerField()    #表示订单的状态
    from_user_id = models.CharField(max_length = 100)
    to_host_id = models.CharField(max_length = 100)  
    from_user_icon = models.CharField(max_length=100)
    to_host_icon = models.CharField(max_length = 100)
    intro_and_question = models.CharField(max_length = 400)          #介绍情况和问题
    appointment_time = models.CharField(max_length = 200)      #约定的时间和时间长度
    appointment_init_time = models.DateTimeField(null = True)   #订单创建的时间
    recommend_info = models.CharField(max_length = 200, null = True)       #分享者回复的消息
    recommend_begin_time = models.DateTimeField( null = True)                    #建议的时间
    recommend_end_time = models.DateTimeField( null = True)                    #建议的时间
    recommend_length = models.FloatField( null = True)                     #建议的时长
    recommend_payment = models.FloatField( null = True)                    #每小时多少钱
    recommend_salary = models.FloatField( null = True)                      #总共多少钱
    feature_id = models.CharField(max_length = 100)            #feature_id
    appointment_id = models.CharField(max_length=100)     #唯一的订单号-》


    def generate_id(self):
        tmp_id = ""
        ymd = datetime.datetime.now().strftime("%Y%m%d")
        tmp_id = tmp_id + ymd
        host = Host.objects.get(id=self.to_host_id)
        tmp_id = tmp_id + binascii.b2a_hex(host.id)[:6]
        appointment_number = str(Appointment.objects.count())
        app_num_length = appointment_number
        tmp_id = tmp_id +str(random.random())[-2:]+'0'* (5-app_num_length) + binascii.b2a_hex(host.id)[:6]
        return tmp_id



    def format_dict_on_manage(self):
        tmp_dict = self.format_dict()
        host = Host.objects.get(id= tmp_dict['to_host_id'])

        tmp_dict['host_name'] = host.username
        tmp_dict['host_motto'] = host.motto
        return tmp_dict

    def format_dict(self):
        tmp_dict = {}

        tmp_dict['id']  = self.id
        tmp_dict['state']  = self.state
        tmp_dict['from_user_id']  = self.from_user_id
        tmp_dict['to_host_id']  = self.to_host_id
        tmp_dict['from_user_icon']  = self.from_user_icon
        tmp_dict['to_host_icon']  = self.to_host_icon
        tmp_dict['intro_and_question']  = self.intro_and_question
        tmp_dict['appointment_time']  = self.appointment_time
        tmp_dict['recommend_info']  = self.recommend_info
        tmp_dict['recommend_begin_time']  = self.recommend_begin_time
        tmp_dict['recommend_end_time']  = self.recommend_end_time
        tmp_dict['recommend_length']  = self.recommend_length
        tmp_dict['appointment_init_time']  = self.appointment_init_time
        tmp_dict['appointment_id']  = self.appointment_id
        appt_feature = Feature.objects.get(id=self.feature_id).f_name
        tmp_dict['feature_name'] = appt_feature

        return tmp_dict
    
    def get_appointment_messages(self):
        messages = Message.objects.filter(extra_id = appointment.id, message_type = MESSAGE_TYPE.APPOINTMENT_COMM).order_by("upload_time")
        result = []
        for msg in messages:
            tmp_msg = {}
            from_user = Host.objects.get(id = msg.from_user )
            tmp_msg['from_user_name'] = from_user.username
            tmp_msg['user_icon'] = from_user.icon
            tmp_msg['message'] = msg.content
            result.append(tmp_msg)

        return result
            