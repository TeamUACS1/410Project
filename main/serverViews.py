from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import urllib2
import urllib
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows

import base64

def getPostsFromServers(request):
	context = RequestContext(request)
	url = 'http://thought-bubble.herokuapp.com/main/getposts/'
	
	string = "Basic "+ base64.b64encode("btrinh:127.0.0.1:a")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)

	posts = []
	for key in data["posts"]:
		posts.append(key)
	
		
	return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)


def searchPostId(request):
	context = RequestContext(request)
	posts = []
	if(request.method == 'POST'):
		postguid1 = request.POST.get("postguid1", "")
		
		url = 'http://thought-bubble.herokuapp.com/main/getapost/?postid='+ postguid1
		
		string = "Basic "+ base64.b64encode("admin:host:admin")
		request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
		contents = urllib2.urlopen(request).read()

		data = json.loads(contents)
		
		posts = []
		for key in data["posts"]:
			
			posts.append(key)
	
		
		return render_to_response('main/searchpostid.html', {'posts': posts}, context)
	return render_to_response('main/searchpostid.html', context)

def specificauthorposts(request):
	context = RequestContext(request)
	
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		url = 'http://thought-bubble.herokuapp.com/main/getauthorposts/?authorid='+ authorguid1 
		
		string = "Basic "+ base64.b64encode("admin:host:admin")
		request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
		contents = urllib2.urlopen(request).read()

		data = json.loads(contents)
		
	

		posts = []
		for key in data["posts"]:
			posts.append(key)
	
		
		return render_to_response('main/searchauthorpost.html', {'posts': posts}, context)
	return render_to_response('main/searchauthorpost.html', context)


def currentlyauthuser(request):
	context = RequestContext(request)


	url = 'http://thought-bubble.herokuapp.com/main/author/posts2/'
	
	string = "Basic "+ base64.b64encode("admin:host:admin")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	


	posts = []
	for key in data["posts"]:
		posts.append(key)

	
	return render_to_response('main/getcurrentauthuser.html', {'posts': posts}, context)

def iffriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		authorguid2 = request.POST.get("authorguid2", "")
		author_list = authorguid2.split(" ")
		author_string = []
		for authors in author_list:
			author_string.append(str(authors))
		

		post_req = {}
		post_req["query"] = "friends"
		post_req["user"] = authorguid1
		post_req["authors"] = author_string

		data = json.dumps(post_req)
		url = 'http://thought-bubble.herokuapp.com/main/checkfriends/?user=' + authorguid1
	

		request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*"})
		contents = urllib2.urlopen(request).read()

		data = json.loads(contents)
		names = []
		for key,value in data.iteritems():
			names.append(value)
		
		print names
		names.pop(0)
		friendee = names[1] + " is friends with:"
		names.pop(1)
		return render_to_response('main/if_friends.html', {'posts': names, 'friendee': friendee}, context)

	return render_to_response('main/if_friends.html', context)

def friendreq(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		displayname = request.POST.get("displayname", "")
		hosts = "http://thought-bubble.herokuapp.com/"
		authorguid2 = request.POST.get("authorguid2", "")
		friend_display = "random"
		friend_url = "random"

		jsonreq = {}
		jsonreq["author"] = {}
		jsonreq["author"]["id"] = authorguid1
		jsonreq["author"]["host"] = hosts
		jsonreq["author"]["displayname"] = displayname

		jsonreq["friend"] = {}
		jsonreq["friend"]["id"] = authorguid2
		jsonreq["friend"]["host"] = hosts
		jsonreq["friend"]["displayname"] = friend_display
		jsonreq["friend"]["url"] = friend_url

		jsonreq["query"] = "friendrequest"

		data = json.dumps(jsonreq)
		url = 'http://thought-bubble.herokuapp.com/main/newfriendrequest/'
	

		request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*"})
		contents = urllib2.urlopen(request).read()

		#data = json.loads(contents)

		print contents

		return render_to_response('main/othernodefriendreq.html', {'posts': contents} ,context)
	return render_to_response('main/othernodefriendreq.html' ,context)

def getpostifFOAF(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		postid = request.POST.get("postid", "")
		authorid = request.POST.get("authorid", "")
		host = "http://thought-bubble.herokuapp.com/"
		authorids = request.POST.get("authorids", "")

		author_list = authorids.split(" ")
		author_string = []
		for authors in author_list:
			author_string.append(str(authors))

		jsonreq = {}
		jsonreq["id"] = postid
		jsonreq["author"] = {}
		jsonreq["author"]["id"] = authorid
		jsonreq["author"]["host"] = host
		jsonreq["author"]["displayname"] = "random"

		jsonreq["friends"] = author_string

		jsonreq["query"] = "getpost"

		url = 'http://thought-bubble.herokuapp.com/main/Foafvis/'
		
		data = json.dumps(jsonreq)
		
		request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*"})
		contents = urllib2.urlopen(request).read()

		data = json.loads(contents)
		print data
		return render_to_response('main/foafothernode.html', {'posts': data} ,context)
	return render_to_response('main/foafothernode.html' ,context)
