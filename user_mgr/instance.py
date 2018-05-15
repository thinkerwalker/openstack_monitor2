from . import common
from . import libvirt_data
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests
import json

def get_token(os_project_name,username,password):
    content=common.glb_openstack()
    content['OS_USERNAME']=username
    content['OS_PASSWORD']=password
    content['OS_PROJECT_NAME']=os_project_name
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('nocatalog', ''),
    )
    data = '{ "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": "%s"},"name": "%s", "password": "%s"} } }, "scope": { "project": { "domain": { "name": "%s" }, "name":  "%s" } } }}' % (content['OS_USER_DOMAIN_NAME'],content['OS_USERNAME'],content['OS_PASSWORD'],content['OS_PROJECT_DOMAIN_NAME'],content['OS_PROJECT_NAME'])
    response = requests.post('%s/auth/tokens?nocatalog' %(content['OS_AUTH_URL']), headers=headers, data=data)
    print(response.status_code)
    if response.status_code == 201:
        return response.headers['X-Subject-Token']
    else:
        return 0

def instance_list(request):
    content=common.glb_openstack()
    #未认证或用户密码错误则显示401
    headers = {
        'X-Auth-Token': '%s' %(request.session.get('token')) ,
    }
    response = requests.get('%s/servers/detail'%(content['OS_COMPUTE_API']), headers=headers)
    # print(response.status_code)
    # print(request.session['token'])
    servers_list=[]
    server_status_num={"ACTIVE":0,"SHUTOFF":0}
    if response.status_code != 200:
        print('获取失败')
        try:
            del request.session['id']
            del request.session['token']
        except KeyError:
            pass
        return render(request,'401.html')
    else:
        # print(request.session['token'])
        instance_list_obj=json.loads(response.text)
        for server in instance_list_obj['servers']:
            if server['status']=='ACTIVE':
                server_status_num["ACTIVE"]=server_status_num["ACTIVE"]+1
            else:
                server_status_num["SHUTOFF"]=server_status_num["SHUTOFF"]+1
                # server_status_num["%s"%(server['status'])]=server_status_num["%s"%(server['status'])]+1
            for address in server['addresses']['external']:
                print(type(address))
                print(address['addr'])
                s={"name":"%s" %(server['name']),"status":"%s" %(server['status']),"id":"%s" %(server['id']),"IP":"%s"%(address['addr'])}
                servers_list.append(s)
        print(servers_list)
        print(server_status_num)
        return render(request,'instance_list.html',{'servers_list':servers_list,'server_status_num':server_status_num})

def instance_detail(request):
    instance_id=request.GET['instance_id']
    content = common.glb_openstack()
    # 未认证或用户密码错误则显示401
    headers = {
        'X-Auth-Token': '%s' % (request.session.get('token')),
    }
    response = requests.get('%s/servers/%s' % (content['OS_COMPUTE_API'],instance_id), headers=headers)
    # print(response.status_code)
    servers_list = []
    if response.status_code != 200:
        print('获取失败')
        try:
            del request.session['id']
        except KeyError:
            pass
        return render(request, '401.html')
    else:
        # print(request.session['token'])
        instance_detail_obj= json.loads(response.text)
        IP=instance_detail_obj['server']['addresses']['external'][0]['addr']
        name=instance_detail_obj['server']['name']
        hypervisor_host=instance_detail_obj['server']['OS-EXT-SRV-ATTR:hypervisor_hostname']
        status=instance_detail_obj['server']['status']
        instance_name=instance_detail_obj['server']['OS-EXT-SRV-ATTR:instance_name']
        #列出实例类型，包括cpu个数，mem大小
        flavor_id = instance_detail_obj['server']['flavor']['id']
        flavor_response=requests.get('%s/flavors/%s' % (content['OS_COMPUTE_API'],flavor_id), headers=headers)
        flavor_obj=json.loads(flavor_response.text)
        disk_size=flavor_obj['flavor']['disk']
        mem_total=flavor_obj['flavor']['ram']
        vcpus = flavor_obj['flavor']['vcpus']
        flavor_name=flavor_obj['flavor']['name']
        swap_total=flavor_obj['flavor']['swap']
        if swap_total == "":
            swap_total=0
        # 列出镜像相关信息
        image_id = instance_detail_obj['server']['image']['id']
        image_response=requests.get('%s/images/%s' % (content['OS_COMPUTE_API'],image_id), headers=headers)
        image_obj=json.loads(image_response.text)
        image_name=image_obj['image']['name']

        instance_detail={"name":name,"instance_name":instance_name,"vcpus":vcpus,"mem_total":mem_total,"IP":IP,"disk_size":disk_size,"flavor_type":flavor_name,"image_name":image_name,"hypervisor_host":hypervisor_host,"status":status}
        print(instance_detail)
        # return HttpResponse(IP+image_id+' '+flavor_id+" "+ str(flavor_obj['flavor']['disk']))
        return render(request,'instance_detail.html',{"instance_detail":instance_detail})
def instance_detail_ajax(request):
    hypervisor_host=request.POST.get('hypervisor_host')
    instance_name=request.POST.get('instance_name')
    instance_data=libvirt_data.get_data(hypervisor_host,instance_name)
    #message = {"status": 200,"hypervisor_host":hypervisor_host}
    message=instance_data
    print(instance_data)
    return JsonResponse(message)
