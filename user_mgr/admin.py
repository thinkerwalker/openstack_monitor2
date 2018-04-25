# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin


# Register your models here.
# class UserAdmin(admin.models):
#     list_display = ('id', 'username','password')

admin.site.register(User)