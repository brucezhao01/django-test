# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib, sys 
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from models import User,Group,FilePath

sys.setdefaultencoding('utf-8')

m = hashlib.md5()


class UserFormLogin(forms.Form):
	username = forms.CharField(label='用户名', max_length=100)
	password = forms.CharField(label='密码', widget=forms.PasswordInput())
	
def login(request):
	if request.method == "POST":
		LoginUser = ""
		whichGroup = ""
		uf = UserFormLogin(request.POST)
		if uf.is_valid():
			#获取表单信息
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			userResult = User.objects.filter(name=username,passwd=password)
			if (len(userResult)>0): 
				loginUser = username
				m.update(username)
				request.session['userid']= str(userResult[0].userid) + username
				request.session['username'] = loginUser
				
				groups = User.objects.get(name=loginUser).groups.all()
				whichGroup = ''
				for i in groups:
					whichGroup = whichGroup + i.name + "|"
				whichGroup = whichGroup[:-1]
				request.session['fkuser_group'] = whichGroup
				return HttpResponseRedirect('/fankuang/landing')
			else:
				return HttpResponse("该用户不存在")
	else:
		uf = UserFormLogin()
		return render_to_response("fkuserlogin.html",{'uf':uf})
		
def landing(request):
	if request.session.has_key('username'):
		username = request.session['username']
		group = request.session['fkuser_group']
		AllGroups = group.split('|')
		fileList = []
		allFiles = FilePath.objects.all()
		for i in AllGroups:
			for j in allFiles:
				if j.group.name == i:
					fileList.append(j)
		media = 'media'
		return render(request, 'landing.html', {"username" : username,'group':group,'media':media,'fileList':fileList})
	else:
		uf = UserFormLogin()
		return render_to_response("fkuserlogin.html",{'uf':uf})
