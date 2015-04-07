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



#Create a get for the public posts hosted on group4's database
#Requires Auth hence the headers
#Then returns the posts to the show_other_server_posts.html page so the posts are displayed
def getPostsFromServers(request):
	context = RequestContext(request)
	url = 'http://thought-bubble.herokuapp.com/main/api/getposts/'
	
	string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	posts = []


	for key in data["posts"]:
		posts.append(key)
	
	url = 'http://cs410.cs.ualberta.ca:41074/service/posts/'
	string = "Basic "+ base64.b64encode("admin:admin")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	for key in data["posts"]:
		posts.append(key)
	
	for post in posts:
		print post
		post['numberComments'] = len(post['comments'])
	return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)

#Grabs all the comments for a server
def getOtherServerComments(request,post_guid):
	context = RequestContext(request)
	posts = []
	postguid1 = post_guid
	try:
		url = 'http://thought-bubble.herokuapp.com/main/api/getapost/?postid='+ postguid1
		string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
		request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
		contents = urllib2.urlopen(request).read()
	except urllib2.HTTPError, e:
		print e.code
		print e.msg

	try:
		url = "http://cs410.cs.ualberta.ca:41074/service/posts/"+ postguid1 + "/"			
		string = "Basic "+ base64.b64encode("admin:admin")
		request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
		contents = urllib2.urlopen(request).read()
	except urllib2.HTTPError, e:
		print e.code
		print e.msg
	
	data = json.loads(contents)
	try:
		for key in data["posts"]:
			error = ""
			posts.append(key)
	except:
		posts = []
		error = data['message']

	for post in posts:
		print post
	return render_to_response('main/serverPostsComments.html', {'posts': posts}, context)

#Create a get for a specific post ID hosted on group4's database
#Requires Auth hence the headers
#Then returns the post to the searchpostid.html page so the post is displayed
#Only do so if the form on the page is posted so you can retrieve variables
def searchPostId(request):
	context = RequestContext(request)
	posts = []
	if(request.method == 'POST'):
		postguid1 = request.POST.get("postguid1", "")
		hostchoice = request.POST.get("hostchoice", "")
		
		if(hostchoice == "1"):
			url = 'http://thought-bubble.herokuapp.com/main/api/getapost/?postid='+ postguid1
			string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
			request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
			#contents = urllib2.urlopen(request).read()
		else:
			url = "http://cs410.cs.ualberta.ca:41074/service/posts/"+ postguid1 + "/"			
			string = "Basic "+ base64.b64encode("admin:admin")
			request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
		
		
		try:
			contents = urllib2.urlopen(request).read()	
			data = json.loads(contents)
			try:
				for key in data["posts"]:
					error = ""
					posts.append(key)
			except:
				posts = []
				error = data['message']
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			error = "No such post."

		
		
		
		
		
		return render_to_response('main/searchpostid.html', {'posts': posts, 'error': error, 'postguid':postguid1}, context)
	return render_to_response('main/searchpostid.html', context)


#Create a get for a specific author ID hosted on group4's database to fetch all the author's posts
#Requires Auth hence the headers
#Then returns the posts to the searchauthorpost.html page so the posts are displayed
#Only do so if the form on the page is posted so you can retrieve variables
def specificauthorposts(request):
	context = RequestContext(request)
	
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		hostchoice = request.POST.get("hostchoice", "")
		if(hostchoice == "1"):
			url = 'http://thought-bubble.herokuapp.com/main/api/getpostsbyauthor/?authorid='+ authorguid1 
			
			string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
			request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
		else:
			url = "http://cs410.cs.ualberta.ca:41074/service/author/"+authorguid1+"/posts/" 
			
			string = "Basic "+ base64.b64encode("admin:admin")
			request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
		posts = []
		error = ""
		try:
			contents = urllib2.urlopen(request).read()
			data = json.loads(contents)
			for key in data["posts"]:
				posts.append(key)
		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			error = "User doesn't exist"

		
		
		
	
		
		return render_to_response('main/searchauthorpost.html', {'posts': posts, 'error': error}, context)
	return render_to_response('main/searchauthorpost.html', context)

#Create a get for the currently auth'ed user, hosted on group4's database, to fetch all the author's posts
#Requires Auth hence the headers
#Then returns the posts to the getcurrentauthuser.html page so the posts are displayed
#Only do so if the form on the page is posted so you can retrieve variables
def currentlyauthuser(request):
	context = RequestContext(request)


	url = 'http://thought-bubble.herokuapp.com/main/api/author/posts2/'
	
	string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	posts = []
	for key in data["posts"]:
		posts.append(key)

	
	return render_to_response('main/getcurrentauthuser.html', {'posts': posts}, context)


#Create a post with an author's id and a list of other author ids and filters for the original author's friends from the list
#This is a POST hence the headers
#Then returns the friend's ids to the if_friends.html page so the ids are displayed
#Only do so if the form on the page is posted so you can retrieve variables
def iffriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		authorguid2 = request.POST.get("authorguid2", "")
		hostchoice = request.POST.get("hostchoice", "")
		author_list = authorguid2.split(" ")
		author_string = []
		for authors in author_list:
			author_string.append(str(authors))
		

		post_req = {}
		post_req["query"] = "friends"
		post_req["authors"] = author_string

		if(hostchoice == "1"):
			post_req["user"] = authorguid1
			data = json.dumps(post_req)
			url = 'http://thought-bubble.herokuapp.com/main/api/checkfriends/?user=' + authorguid1
		

			request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*"})
			

		else:
			post_req["author"] = authorguid1
			data = json.dumps(post_req)
			
			
			url = "http://cs410.cs.ualberta.ca:41074/service/friends/"+authorguid1+"/"
			string = "Basic "+ base64.b64encode("admin:admin")
			request = urllib2.Request(url=url, data=data, headers={"Authorization" : string, 'Host': "cs410.cs.ualberta.ca:41074","Content-Type" : "application/json", "Accept": "*/*"})
		
		names = []
		try:
			contents = urllib2.urlopen(request).read()
			data = json.loads(contents)

			
			friendee = ""
			for key,value in data.iteritems():
				names.append(value)
			
			if(len(names) != 1):
				names.pop(0)
				friendee = names[1] + " is friends with:"
				names.pop(1)
			else:
				friendee = names[0]
				del names[:]

		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			friendee = "Queried author not found"

		return render_to_response('main/if_friends.html', {'posts': names, 'friendee': friendee}, context)

	return render_to_response('main/if_friends.html', context)

#Create a post with two author id and the adder's displayname to create a friend request
#This is a POST hence the headers
#Then returns the status message to the othernodefriendreq.html page so it can be displayed
#Only do so if the form on the page is posted so you can retrieve variables
def friendreq(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		authorguid1 = request.POST.get("authorguid1", "")
		displayname = request.POST.get("displayname", "")
		hosts = "http://thought-bubble.herokuapp.com/"
		authorguid2 = request.POST.get("authorguid2", "")
		hostchoice = request.POST.get("hostchoice", "")
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

		if(hostchoice == "1"):
			url = 'http://thought-bubble.herokuapp.com/main/api/newfriendrequest/'
			request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*"})
			

		else:
			url = "http://cs410.cs.ualberta.ca:41074/service/friendrequest/"
			string = "Basic "+ base64.b64encode("admin:admin")			
			request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*","Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
		try:
			contents = urllib2.urlopen(request).read()
			if (contents == "200 OK" or "{}"):
				contents = "Friend request sent!"
		
		except urllib2.HTTPError, e:
				contents = "Users not in the database!"

		return render_to_response('main/othernodefriendreq.html', {'posts': contents} ,context)
	return render_to_response('main/othernodefriendreq.html' ,context)

#Create a post with a postid, an author id and a list or author ids to check for FOAF 
#This is a POST hence the headers
#Then returns the post to the foafothernode.html page so it can be displayed
#Only do so if the form on the page is posted so you can retrieve variables
def getpostifFOAF(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		postid = request.POST.get("postid", "")
		authorid = request.POST.get("authorid", "")
		
		authorids = request.POST.get("authorids", "")
		hostchoice = request.POST.get("hostchoice", "")

		author_list = authorids.split(" ")
		author_string = []
		for authors in author_list:
			author_string.append(str(authors))

		jsonreq = {}
		jsonreq["id"] = postid
		jsonreq["author"] = {}
		jsonreq["author"]["id"] = authorid
		jsonreq["author"]["displayname"] = "random"
		jsonreq["friends"] = author_string
		jsonreq["query"] = "getpost"

		if(hostchoice == "1"):
			host = "http://thought-bubble.herokuapp.com/"
			jsonreq["author"]["host"] = host

			url = 'http://thought-bubble.herokuapp.com/main/api/Foafvis/'
			
			data = json.dumps(jsonreq)
			
			string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
			request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*","Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
			
		else:
			host = "http://cs410.cs.ualberta.ca"
			jsonreq["author"]["host"] = host

			url = 'http://cs410.cs.ualberta.ca:41074/service/foaf/getposts/'
			
			data = json.dumps(jsonreq)
			
			string = "Basic "+ base64.b64encode("admin:admin")
			
			request = urllib2.Request(url=url, data=data, headers={"Content-Type" : "application/json", "Accept": "*/*","Authorization" : string, 'Host': 'cs410.cs.ualberta.ca:41074'})
		
		error = ""
		try:
			contents = urllib2.urlopen(request).read()
			data = []
			try:
				data = json.loads(contents)
				if(hostchoice != "1"):
					posts = []
					for key in data["posts"]:
						posts.append(key)
					data = posts[0]
				print data
			except:
				data = []
				error = contents
			
		
		except urllib2.HTTPError, e:
				error = "Bad post ID"
				data = []
		

		

		
		return render_to_response('main/foafothernode.html', {'posts': data, 'error': error} ,context)
	return render_to_response('main/foafothernode.html' ,context)

def getallauthors(request):
	context = RequestContext(request)
	url = 'http://thought-bubble.herokuapp.com/main/api/getallauthors/'
	
	string = "Basic "+ base64.b64encode("dan:cmput410project15.herokuapp.com:dan")
	request = urllib2.Request(url, headers={"Authorization" : string, 'Host': 'thought-bubble.herokuapp.com'})
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	posts = []
	for key in data["authors"]:
		posts.append(key)
	
	url = "http://cs410.cs.ualberta.ca:41074/service/author/"
	request = urllib2.Request(url)
	contents = urllib2.urlopen(request).read()

	data = json.loads(contents)
	
	for key in data:
		
		posts.append(key)

	return render_to_response('main/show_other_server_authors.html', {'posts': posts}, context)
