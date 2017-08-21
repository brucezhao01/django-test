# -* coding:utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from zls import views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^fankuang/super/', admin.site.urls), ##管理员界面
	url(r'^$',views.login),
	url(r'fankuang/login$', views.login),  ##登录界面
	url(r'^fankuang/landing$', views.landing), ##登录后的界面
	url(r'^fankuang/logout$', views.login), ##登出，跳转至登录界面
	
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)\
+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
