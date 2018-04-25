# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def glb_openstack():
    content={}
    content['OS_PROJECT_DOMAIN_NAME']='default'
    content['OS_USER_DOMAIN_NAME']='default'
    content['OS_PROJECT_NAME']='admin'
    content['OS_USERNAME']='admin'
    content['OS_PASSWORD']='admin'
    content['OS_AUTH_URL']='http://192.168.10.10:35357/v3'
    content['OS_IDENTITY_API_VERSION']='3'
    content['OS_IMAGE_API_VERSION']='2'
    content['OS_COMPUTE_API']='http://192.168.10.10:8774/v2.1'
    return content
