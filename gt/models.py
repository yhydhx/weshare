# coding:utf-8

import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField
from django import forms
from settings import EMAIL_HOST_USER
from django.shortcuts import render
from django.template import Context

#mail server
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context, loader
from gt.settings import *

class Host(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    # 以上为必选信息
    gender = models.IntegerField(default=1, blank=True)  # 1是男生0是女生
    motto = models.CharField(max_length=100, blank=True)
    introduction = models.CharField(max_length=2000, blank=True)
    icon = models.CharField(max_length=200)
    orders = models.IntegerField(default=0)
    service_time = models.CharField(max_length=100, default=True)
    max_payment = models.FloatField(default=0)
    min_payment = models.FloatField(default=0)
    h_school = models.CharField(max_length=200)
    state = models.IntegerField(default=0)  # normal user  => 0  examing => 1  sharer => 2

    birth = models.CharField(blank=True, max_length=100)
    qq_number = models.CharField(blank=True, max_length=20)
    wechat = models.CharField(blank=True, max_length=20)
    forget_string = models.CharField(blank=True, max_length=200)     # 这个forget_string用来进行找回密码验证的。

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
                tag = tag + " " + str(v)

            each_host.image = "/files/icons/" + each_host.icon.split("/")[-1]
            each_host.min_payment = int(each_host.min_payment)
            each_host.tag = tag

        Info = {}
        Info['hosts'] = hosts
        Info['topics'] = d_topic_detail.values()
        print Info['topics']
        return Info


class Province(models.Model):
    p_name = models.CharField(max_length=100)
    p_id = models.IntegerField()


class School(models.Model):
    s_name = models.CharField(max_length=200)
    s_province = models.CharField(max_length=200)
    s_display_index = models.IntegerField()
    s_student_number = models.IntegerField()


class Topic(models.Model):
    t_name = models.CharField(max_length=200)
    t_click = models.IntegerField(default=0)
    t_tag = models.CharField(max_length=100, null=True)


class Feature(models.Model):
    f_name = models.CharField(max_length=200)
    f_topic = models.CharField(max_length=100)


class Host_Topic(models.Model):
    host_id = models.CharField(max_length=100)
    t_id = models.CharField(max_length=100)
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
    #m_upload_time = models.DateField(null=True)


class Document(models.Model):
    d_menu = models.CharField(max_length=100)
    d_name = models.CharField(max_length=100)
    d_text = models.TextField()
    d_index = models.IntegerField()  # 将不同的话题区分开来


class Mail(models.Model):
    subject = models.CharField(max_length=200)
    from_email = models.CharField(max_length=200)
    to_email = models.CharField(max_length=200)
    host_id = models.CharField(max_length=200)
    admin_id = models.CharField(max_length=200)
    content = models.TextField()
    is_success = models.IntegerField()
    
    def sendMail(self, subject,to,content):
    #to = ['yhydhx@126.com']

        context = {"content": content}

        email_template_name = 'backEnd/blankTemp.html'
        t = loader.get_template(email_template_name)

        from_email = EMAIL_HOST_USER

        html_content = t.render(Context(context))
        # print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    def forgotPassword(self,subject,to,content):
        context = {"content": content}

        email_template_name = 'backEnd/forgotPasswordTemp.html'
        t = loader.get_template(email_template_name)

        from_email = EMAIL_HOST_USER

        html_content = t.render(Context(context))
        #print html_content
        msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        msg.send()

class Message(models.Model):
    from_user = models.CharField(max_length=100)
    to_user = models.CharField(max_length=100)
    message_type = models.IntegerField()
    upload_time = models.DateField()
