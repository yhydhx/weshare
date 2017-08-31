# coding:utf-8

from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField
from django import forms
from django.shortcuts import render
from django.template import Context

# mail server
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template import Context, loader
from gt.settings import *


import hashlib,binascii,datetime,random


class Item(models.Model):
	item_type = models.CharField(max_length = 20)
	item_id = models.CharField(max_length = 200)
	item_name = models.CharField(max_length = 200)
	item_price = models.FloatField()
	item_amount = models.IntegerField()
	item_crawl_date = models.DateTimeField()



class Select(models.Model):
	item_id  =  models.CharField(max_length= 200)
	username  =  models.CharField(max_length=200)