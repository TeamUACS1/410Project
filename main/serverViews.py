from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import urllib2
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows

def getPostsFromServers(request):
	context = RequestContext(request)
	url = 'http://thought-bubble.herokuapp.com/main/getposts/'
	serialized_data = urllib2.urlopen(url).read()
	data = json.loads(serialized_data)

	posts = []
	for key in data["posts"]:
		posts.append(key)
	
		
	return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)


def ifFriends(request):
	context = RequestContext(request)
	data = ""
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		authorguid2 = request.POST.get("authorguid2", "")
		url = 'http://thought-bubble.herokuapp.com/main/getfriendstatus/?user='+ authorguid1 +'/'+authorguid2 + '/'
		serialized_data = urllib2.urlopen(url).read()
		data = json.loads(serialized_data)
		data = data["friends"]
	#url = 'http://thought-bubble.herokuapp.com/main/getfriendstatus/?user=ef6728777e36445d8d45d9d5125dc4c6/9e4ac346d9874b7fba14f27b26ae45bb/'

	

	#return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)
	#posts = []
	#for key in data["posts"]:
	#	posts.append(key)
	
		
	return render_to_response('main/if_friend.html', {'posts': data}, context)

def friendList(request):
	context = RequestContext(request)
	
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		authorguid2 = request.POST.get("authorguid2", "")
		url = 'http://thought-bubble.herokuapp.com/main/getfriendstatus/?user='+ authorguid1 +'/'+authorguid2 + '/'
		serialized_data = urllib2.urlopen(url).read()
		data = json.loads(serialized_data)
		data = data["friends"]
	#url = 'http://thought-bubble.herokuapp.com/main/getfriendstatus/?user=ef6728777e36445d8d45d9d5125dc4c6/9e4ac346d9874b7fba14f27b26ae45bb/'

	

	#return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)
	#posts = []
	#for key in data["posts"]:
	#	posts.append(key)
	
		
	return render_to_response('main/if_friend.html', {'posts': data}, context)