# coding:utf-8

import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField
from django import forms


class Host(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    # 以上为必选信息
    gender = models.IntegerField(default=1, blank=True)  # 1是男生0是女生
    motto = models.CharField(max_length=100, blank=True)
    introduction = models.CharField(max_length=2000, blank=True)
    icon = models.CharField(max_length=100, blank=True)
    orders = models.IntegerField(default=0)
    service_time = models.CharField(max_length=100, default=True)
    max_payment = models.FloatField(default=0)
    min_payment = models.FloatField(default=0)
    state = models.IntegerField(default=0)  # normal user  => 0  examing => 1  sharer => 2
    h_school = models.CharField(max_length=200)
    def get_all_features(self):
        host_topics =  Host_Topic.objects.filter(host_id=self.id)
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
        
        for t_id,value in d_topic_feature.items():
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
    t_tag = models.CharField(max_length=200)


class Feature(models.Model):
    f_name = models.CharField(max_length=200)
    f_topic = models.CharField(max_length=100)


class Host_Topic(models.Model):
    host_id = models.CharField(max_length=100)
    t_id = models.CharField(max_length=100)
    f_id = models.CharField(max_length=100)  # 关系库


class Certificate(models.Model):   # igno
    host_id = models.CharField(max_length=100)
    c_name = models.CharField(max_length=200)
    c_state = models.IntegerField()


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
