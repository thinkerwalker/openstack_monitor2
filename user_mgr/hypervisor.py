from . import common
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests
import json

def hypervisor_list(request):
    # return HttpResponse('abc')
    content=common.glb_openstack()
    # 未认证或用户密码错误则显示401
    headers = {
        'X-Auth-Token': '%s' % (request.session.get('token')),
    }
    response = requests.get('%s/os-hypervisors' % (content['OS_COMPUTE_API']), headers=headers)
    if response.status_code != 200:
        print('获取失败')
        try:
            del request.session['id']
            del request.session['token']
        except KeyError:
            pass
        return render(request,'401.html')
    else:
        hypervisor_list_obj=json.loads(response.text)

    return render(request,'hypervisor_list.html',{"hypervisor_list":hypervisor_list_obj['hypervisors']})

def hypervisor_detail(request):
    hypervisor_id=request.GET.get('hypervisor_id')
    content = common.glb_openstack()
    # 未认证或用户密码错误则显示401
    headers = {
        'X-Auth-Token': '%s' % (request.session.get('token')),
    }
    response = requests.get('%s/os-hypervisors/%s' % (content['OS_COMPUTE_API'],hypervisor_id), headers=headers)
    if response.status_code != 200:
        print('获取失败')
        try:
            del request.session['id']
            del request.session['token']
        except KeyError:
            pass
        return render(request, '401.html')
    else:
        # print(request.session['token'])
        hypervisor_obj = json.loads(response.text)
        cpu_info_obj= json.loads(hypervisor_obj['hypervisor']['cpu_info'])
        response_hy_instance_list = requests.get('%s/os-hypervisors/%s/servers' % (content['OS_COMPUTE_API'], hypervisor_obj['hypervisor']['hypervisor_hostname']), headers=headers)
        hy_instance_list_obj = json.loads(response_hy_instance_list.text)
        print(hy_instance_list_obj)

    return render(request, 'hypervisor_detail.html', {"hypervisor": hypervisor_obj['hypervisor'],"cpu_info":cpu_info_obj,"hy_instance_list":hy_instance_list_obj['hypervisors'][0]})