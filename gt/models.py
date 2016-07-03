import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField
from django import forms
from django.contrib.auth.models import User


class Host(User):
    gender = models.IntegerField(blank=True)
    motto = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    introduction = models.CharField(max_length=2000, blank=True)
    icon = models.CharField(max_length=100, blank=True)
    orders = models.IntegerField(default=0)
    service_time = models.CharField(max_length=100, default=True)
    max_payment = models.FloatField(default=0)
    min_payment = models.FloatField(default=0)
    state = models.IntegerField(default=0)  # normal user  => 0  examing => 1  sharer => 2


class Province(models.Model):
    p_name = models.CharField(max_length=100)
    p_id = models.IntegerField()


class School(models.Model):
    s_name = models.CharField(max_length=200)
    s_province = models.CharField(max_length=200)
    s_link = models.CharField(max_length=100)
    s_student_number = models.CharField(max_length=100)


class Topic(models.Model):
    t_name = models.CharField(max_length=200)
    t_click = models.IntegerField()


class Feature(models.Model):
    f_name = models.CharField(max_length=200)
    f_topic_id = models.CharField(max_length=100)


class Host_Topic(models.Model):
    host_id = models.CharField(max_length=100)
    t_id = models.CharField(max_length=100)
    f_id = models.CharField(max_length=100)


class Certificate(models.Model):
    host_id = models.CharField(max_length=100)
    c_name = models.CharField(max_length=200)
    c_state = models.IntegerField()
