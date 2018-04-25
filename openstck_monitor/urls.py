"""openstck_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user_mgr import  views
from user_mgr import  instance

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^login$', views.login),
    url(r'^login_ajax$', views.login_ajax),
    url(r'^login_out.html$',views.login_out),
    url(r'^index', views.device_list),
    url(r'^device_list/',views.device_list),
    url(r'user_info/',views.user_info),
    url(r'user_update/',views.user_update),
    url(r'^instance_detail$',instance.instance_detail),
    url(r'^influxdb_get_mem_usage.html$',views.influxdb_get_mem_usage),
    url(r'^instance_list$',instance.instance_list),
    url(r'^instance_detail_ajax$',instance.instance_detail_ajax),
]
