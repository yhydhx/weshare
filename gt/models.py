import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms

class Process(models.Model):
    Uid = models.CharField(max_length=100)
    times = models.IntegerField()
    coMethod = models.IntegerField()
    addMoney = models.IntegerField()
    money = models.IntegerField()
    addRobotMoney = models.IntegerField()
    robotMoney = models.IntegerField()
    humanChoose = models.IntegerField()
    robotChoose = models.IntegerField()
    processDate = models.DateTimeField()
    clientIP = models.CharField(max_length=30)
    def date_format(self):
    	self.date = self.date.strftime("%Y-%m-%d")


class Player(models.Model):
    Uid = models.CharField(max_length=100)
    trueName = models.CharField(max_length = 100)
    isTrueName = models.IntegerField()
    uploadTime = models.DateTimeField()
    finalScore = models.IntegerField(null=True )
    finalRobotScore = models.IntegerField(null=True )
    rounds = models.IntegerField(null=True)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class Rule(models.Model):
    ruleName = models.CharField(max_length = 100)
    p1 = models.FloatField()
    p2 = models.FloatField()
    p3 = models.FloatField()
    p4 = models.FloatField()
    maxRound = models.IntegerField()
    minRound = models.IntegerField()
    w = models.FloatField()
