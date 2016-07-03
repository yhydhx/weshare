import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms


class Host(models.Model):
    name = models.CharField(max_length = 100)
    gender = models.IntegerField()
    motto = models.CharField(max_length= 100)
    phone_number = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    introduction = models.CharField(max_length = 1000)
    icon = models.CharField(max_length=100)
    orders = models.IntegerField()
    service_time = models.CharField(max_length=100)
    max_payment = models.FloatField()
    min_payment = models.FloatField()
    state  = models.IntegerField()  #normal user  => 0  examing => 1  sharer => 2

class Province(models.Model):
    p_name = models.CharField(max_length=100)
    p_id = models.IntegerField()

    
class School(models.Model):
    s_name  = models.CharField(max_length=200)
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


class User(models.Model):
    username = models.CharField(max_length = 100)
    #email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    #inviting_code = models.CharField(max_length =50)
    #user_flag = models.SmallIntegerField()