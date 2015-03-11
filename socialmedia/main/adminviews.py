from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
import urllib2
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Users
from main.models import Friends

def approveAuthor(request):
	context =RequestContext(request)
	authors = Users.objects.filter(approved_flag=0)
	return render_to_response('main/show_approval_list.html', {'authors': authors}, context)

def approve(request):
	context =RequestContext(request)
	author= request.POST.get("ID", "")
	authors = Users.objects.get(id=author)
	authors.approved_flag=1
	authors.save()
	return redirect(approveAuthor)

def manageAuthor(request):
	context =RequestContext(request)
	authors = Users.objects.filter()
	return render_to_response('main/show_authors_list.html', {'authors': authors}, context)

def deleteauthor(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		author= request.POST.get("ID", "")
		author =Users(id=author)
		author.delete()
	return redirect(manageAuthor)


def editauthor(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		posts =Posts.objects.filter(id=post)
	return render_to_response('main/edit.html',{'posts': posts}, context)

def save(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		post2= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		date = datetime.now()
		if(flag == "3"):
			private_auth = request.POST.get("private_auth", "")
			post=Posts(id=post,post=post2,author=request.session['user'],privateFlag=flag, extra=private_auth, date=date)
			post.save()
		else:
			post=Posts(id=post,post=post2,author=request.session['user'],privateFlag=flag,date=date)
			post.save()
	return redirect(showposts)
