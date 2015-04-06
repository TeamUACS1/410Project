#Contains all of the functions associated with the admin functionalities
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
import urllib2
import uuid
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows
from main.models import Nodes

#shows the authors that have been approved by the admin. Displays them on a page accesible by the admin
def approveAuthor(request):
	context =RequestContext(request)
	authors = Authors.objects.filter(approved_flag=0)
	return render_to_response('main/show_approval_list.html', {'authors': authors}, context)
def approveHosts(request):
	context =RequestContext(request)
	return render_to_response('main/search_hosts.html', context)

#allows the admin to approve a new user/author to the website after they sign up for an account
def approve(request):
	context =RequestContext(request)
	author= request.POST.get("ID", "")
	authors = Authors.objects.get(id=author)
	authors.approved_flag=1
	authors.save()
	return redirect(approveAuthor)

#Allows the server admin to manage the authors on the website
def manageAuthor(request):
	context =RequestContext(request)
	authors = Authors.objects.filter()
	return render_to_response('main/show_authors_list.html', {'authors': authors}, context)

def manageHosts(request):
	context =RequestContext(request)
	hosts = Nodes.objects.filter()
	return render_to_response('main/show_hosts_list.html', {'hosts': hosts}, context)
#Allows the server admin to delete authors from the website
def deleteauthor(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		author= request.POST.get("ID", "")
		author =Authors(id=author)
		author.delete()
	return redirect(manageAuthor)

#Allows the server admin to edit author information 
def editauthor(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		author= request.POST.get("ID", "")
		author =Authors.objects.filter(id=author)
	return render_to_response('main/edit_authors.html',{'author': author}, context)

#Allows the server admin to save changes made to the author information
def saveauthor(request):
	context = RequestContext(request)
	context =RequestContext(request)
	author= request.POST.get("ID", "")
	authors = Authors.objects.get(id=author)
	password=request.POST.get("password", "")
	encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
	authors.password=encrypted_pass
	authors.save()
	return redirect(manageAuthor)
def addHosts(request):
	approved_flag=1
	host=request.POST.get("searchUser")
	guid = str(uuid.uuid1()).replace("-", "")
	nodes=Nodes(approved_flag=approved_flag,host=host,guid=guid)
	nodes.save()
	

	return redirect(approveHosts)
