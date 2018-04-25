# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=60,unique=True)
    password=models.CharField(max_length=32)
    mobile_phone=models.CharField(max_length=11)
    class Meta:
        verbose_name="用户"
        verbose_name_plural=verbose_name