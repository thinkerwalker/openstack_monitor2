# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.shortcuts import render, HttpResponse
from .models import *
from django.http import JsonResponse
from . import instance
import json
import requests


#login page
def login(request):
    id = request.session.get('id')
    print(id)
    if id:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')

#login for ajax
def login_ajax(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    os_project_name=request.POST.get('os_project_name')
    flag=instance.get_token(os_project_name,username,password)
    if flag == 0:
        message = {"status": 403, "msg": "password error"}
    else:
        message = {"status": 200, "msg": "success"}
        request.session['token'] = flag
        request.session['id'] = flag
    return JsonResponse(message)

#login_out would del session
def login_out(request):
    try:
        del request.session['id']
        del request.session['token']
    except KeyError:
        pass
    return render(request, "login.html")
def device_list(request):
    id = request.session.get('id')
    print("333")
    print(id)
    if id:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')
def user_info(request):
    return render(request,'index.html')
def user_update(request):
    return render(request,'index.html')


# def influxdb_get_mem_usage(request):
#     # params={'db':'libvirtdb','q':'SELECT * FROM guest;'}
#     # r=requests.get('http://192.168.20.16:8086/query',params=params)
#     from . import  influxdb_operation
#     query_string='SELECT * FROM guest;'
#     host='192.168.20.16'
#     result=influxdb_operation.influxdb_query(query_string,host)
#
#     print(result.raw["series"][0]["values"])
#     return HttpResponse(json.dumps(result.raw))
def influxdb_get_mem_usage(request):
    from . import influxdb_operation
    # measurement = 'guest'
    # influxdb_host = '192.168.20.16'
    # host='127.0.0.1'
    # query_string = "SELECT mem_usage FROM %s where host='%s' limit 1;"  % (measurement,host)
    # # query_string ="SELECT mem_usage FROM guest where host='127.0.0.1' limit 1;"
    # print(query_string)
    # result = influxdb_operation.influxdb_query(query_string, influxdb_host)
    # message={}
    # message=result.raw["series"][0]["values"]
    # print(message)
    # message={"time":result.raw["series"][0]["values"][0][0],"value":result.raw["series"][0]["values"][0][1]}
    message={"value":30}
    return JsonResponse(message)

def author_info(request):
    return render(request,'author_info.html')

def monitor_silu(request):
    return render(request,'monitor_silu.html')
