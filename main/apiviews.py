from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import urllib2
import base64
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows
from functools import wraps
from django.conf import settings

#based on tutorial from http://learningdjango.blogspot.ca/2012/04/basic-http-authentication-in-django.html
def basic_http_auth(f):
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION', False):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
            auth = base64.b64decode(auth)
            username, password = auth.split(':')
            if username == settings.BASICAUTH_USERNAME and password == settings.BASICAUTH_PASSWORD:
                return f(request, *args, **kwargs)
            else:
                r = HttpResponse("Auth Required", status = 401)
                r['WWW-Authenticate'] = 'Basic realm="hi"'
                return r
        r = HttpResponse("Auth Required", status = 401)
        r['WWW-Authenticate'] = 'Basic realm="hi"'
        return r
        
    return wrap

@basic_http_auth
def getposts(request):

	lists=[]
	context =RequestContext(request)
	#user = request.session['user']
	posts = Posts.objects.filter(Q(visibility='PUBLIC'))
	for post in posts:
		post2 = {}
		post2['title'] = post.title
		post2['source'] = post.source
		post2['origin']= post.origin
		post2['description'] = post.description
		post2['content-type'] = post.content_type
		post2['content'] = post.content
		post2['pubdate'] = str(post.pubDate)
		post2['guid'] = str(post.guid)
		post2['visability'] = post.visibility
		string = str(post.author).split("guid\":")[1]
		string=string.split(",")[0]
		string=string.split("\"")[1]
		author=Authors.objects.filter(guid=str(string))
		for author in author:
			author2={}
			author2['id'] = str(author.guid)
			author2['host'] = "cmput410project15.herokuapp.com"
			author2['displayname'] = author.displayname
			author2['url'] = "cmput410project15.herokuapp.com/main/author/" + str(author.guid)
			post2['author'] = author2
			post2['comments'] = []
			lists.append(post2)
	return HttpResponse(json.dumps({"posts" : lists}))

@basic_http_auth
def authorposts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts1 = Posts.objects.filter(Q(visibility='PRIVATE') | Q(author=user))
	posts2 = Posts.objects.filter(Q(visibility='PUBLIC'))
	posts3 = Posts.objects.filter(guid='0')
	friends = Friends.objects.raw("select * from main_friends where ((authorguid1 = '"+ user +"') or (authorguid2 = '"+ user +"') and accepted = 1)")	
	friend_list = []
	for friend in friends:
		if ((friend.authorguid1 != request.session['user_guid']) and (friend.authorguid2 == request.session['user_guid'])):
			friend_list.append(friend.authorguid1)
		if ((friend.authorguid2 != request.session['user_guid']) and (friend.authorguid1 == request.session['user_guid'])):
			friend_list.append(friend.authorguid2)
	posts = Posts.objects.filter(guid='0')
	for friend in friend_list:

		author = Authors.objects.filter(guid=friend)
		string=serializers.serialize("json",author,fields=('guid','host','displayname','url'))
		string=str(string).replace("fields","author")
		string=str(string).split("},")[0]
		string=string + "}}]"
		newpost=Posts.objects.filter(Q(author=string) &Q(visibility="FRIENDS"))
		posts3 = posts | newpost
	authors = Posts.objects.raw("select distinct p.id, p.author from main_posts p, main_friends f where p.visibility ='FOAF';")
	user_friend = Friends.objects.raw("select id, authorguid1, authorguid2 from main_friends where authorguid1 = '" + user + "' or authorguid2 = '"+ user +"'; ")
	total_posts = Posts.objects.filter(guid='0')
	looked_up = []
	looked_up.append(user)

	for auth in authors:	
		for fid in user_friend:
			if(str(auth.author) not in looked_up):
				total = Friends.objects.raw("select count(*) from main_friends where ((f.authorguid2 = '"+ str(fid.authorguid1) +"' and '" + str(auth.author) + "' = f.authorguid1) or (f.authorguid1 = '"+ str(fid.authorguid1) +"' and '"+ str(auth.author) +"' = f.authorguid2)); ")	
				totalf = Friends.objects.raw("select count(*) from main_friends where ((f.authorguid2 = '"+ str(fid.authorguid2) +"' and '" + str(auth.author) + "' = f.authorguid1) or (f.authorguid1 = '"+ str(fid.authorguid2) +"' and '"+ str(auth.author) +"' = f.authorguid2)); ")	
				looked_up.append(str(auth.author))
				if (total or totalf):
					posts5=Posts.objects.raw("select p.id from main_posts p where p.author = '"+ str(auth.author) +"' and p.visibility ='FOAF';")
					total_posts = posts5|total_posts
	posts= posts1|posts2|posts3|total_posts
	lists=[]
	for post in posts:
		print post
		post2 = {}
		post2['title'] = post.title
		post2['source'] = post.source
		post2['origin']= post.origin
		post2['description'] = post.description
		post2['content-type'] = post.content_type
		post2['content'] = post.content
		post2['pubdate'] = str(post.pubDate)
		post2['guid'] = str(post.guid)
		post2['visability'] = post.visibility
		string = str(post.author).split("guid\":")[1]
		string=string.split(",")[0]
		string=string.split("\"")[1]
		author=Authors.objects.filter(guid=str(string))
		for author in author:
			author2={}
			author2['id'] = str(author.guid)
			author2['host'] = "cmput410project15.herokuapp.com"
			author2['displayname'] = author.displayname
			author2['url'] = "cmput410project15.herokuapp.com/main/author/" + str(author.guid)
			post2['author'] = author2
			post2['comments'] = []
			lists.append(post2)
	return HttpResponse(json.dumps({"posts" : lists}))

@basic_http_auth
def authorsposts(request,author_guid):
	context = RequestContext(request)
	friends = Authors.objects.filter(guid=author_guid)
	string=serializers.serialize("json",friends,fields=('guid','host','displayname','url'))
	string=str(string).replace("fields","author")
	string=str(string).split("},")[0]
	string=string + "}}]"
	friend = Authors.objects.get(guid=author_guid)
	user = request.session['user_guid']
	users = request.session['user']
	f=Friends.objects.filter((Q(authorguid1=user)&Q(authorguid2=friend)&Q(accepted=str(1)))|(Q(authorguid2=user)&Q(authorguid1=friend)&Q(accepted=str(1))))
	fr=Friends.objects.filter((Q(authorguid1=user)&Q(authorguid2=friend)&Q(accepted=str(0)))|(Q(authorguid2=user)&Q(authorguid1=friend)&Q(accepted=str(0))))
	fo=Follows.objects.filter(authorguid1=user,authorguid2=friend.guid)
	
	if string==users:
		post=Posts.objects.filter(author=string)

	elif f:
		post=Posts.objects.filter(Q(author=string) &( Q(visibility="PUBLIC")|Q(visibility="FRIENDS")))
	elif fr:
		post=Posts.objects.filter(Q(author=string) &( Q(visibility="PUBLIC")|Q(visibility="FRIENDS")))
	elif fo:
		post=Posts.objects.filter(author=string,visibility="PUBLIC")
	else:
		post=Posts.objects.filter(author=string,visibility="PUBLIC")
	lists=[]
	for post in post:
		print post
		post2 = {}
		post2['title'] = post.title
		post2['source'] = post.source
		post2['origin']= post.origin
		post2['description'] = post.description
		post2['content-type'] = post.content_type
		post2['content'] = post.content
		post2['pubdate'] = str(post.pubDate)
		post2['guid'] = str(post.guid)
		post2['visability'] = post.visibility
		string = str(post.author).split("guid\":")[1]
		string=string.split(",")[0]
		string=string.split("\"")[1]
		author=Authors.objects.filter(guid=str(string))
		for author in author:
			author2={}
			author2['id'] = str(author.guid)
			author2['host'] = "cmput410project15.herokuapp.com"
			author2['displayname'] = author.displayname
			author2['url'] = "cmput410project15.herokuapp.com/main/author/" + str(author.guid)
			post2['author'] = author2
			post2['comments'] = []
			lists.append(post2)
	return HttpResponse(json.dumps({"posts" : lists}))



#send specific ID
def getpost(request,post_guid):
	if request.method == 'GET':
		lists=[]
		context =RequestContext(request)
		#user = request.session['user']
		posts = Posts.objects.filter(Q(guid=post_guid))
		for post in posts:
			post2 = {}
			post2['title'] = post.title
			post2['source'] = post.source
			post2['origin']= post.origin
			post2['description'] = post.description
			post2['content-type'] = post.content_type
			post2['content'] = post.content
			post2['pubdate'] = str(post.pubDate)
			post2['guid'] = str(post.guid)
			post2['visibility'] = post.visibility
			string = str(post.author).split("guid\":")[1]
			string=string.split(",")[0]
			string=string.split("\"")[1]
			author=Authors.objects.filter(guid=str(string))
			for author in author:
				author2={}
				author2['id'] = str(author.guid)
				author2['host'] = "cmput410project15.herokuapp.com"
				author2['displayname'] = author.displayname
				author2['url'] = "cmput410project15.herokuapp.com/main/author/" + str(author.guid)
				post2['author'] = author2
				post2['comments'] = []
				lists.append(post2)
		return HttpResponse(json.dumps({"posts" : lists}))

	elif request.method == 'POST' or 'PUT':
		lists =[]
		context = RequestContext(request)
		
		"""
		for post in posts:
			
			post2 = {}
			post2['title'] = post.title
			post2['source'] = post.source
			post2['origin']= post.origin
			post2['description'] = post.description
			post2['content-type'] = post.content_type
			post2['content'] = post.content
			post2['pubdate'] = str(post.pubDate)
			post2['guid'] = str(post.guid)
			post2['visability'] = post.visibility
			string = str(post.author).split("guid\":")[1]
			string=string.split(",")[0]
			string=string.split("\"")[1]
			author=Authors.objects.filter(guid=str(string))
			for author in author:
				author2={}
				author2['id'] = str(author.guid)
				author2['host'] = "cmput410project15.herokuapp.com"
				author2['displayname'] = author.displayname
				author2['url'] = "cmput410project15.herokuapp.com/main/author/" + str(author.guid)
				post2['author'] = author2
				post2['comments'] = []
				lists.append(post2)
			"""

		existingpost = Posts.objects.filter(Q(guid=post_guid))
		if(existingpost):

			date = datetime.now()
			info = json.loads(request.body)
			title = info["title"]
			description = info["description"]
			content = info["content"]
			visibility = info["visibility"]
			author = info["author"]["displayname"]

			string=serializers.serialize("json",Authors.objects.filter(displayname=author),fields=('guid','host','displayname','url'))
			string=str(string).replace("fields","author")
			string=str(string).split("},")[0]
			string=string + "}}]"

			guid = str(uuid.uuid1()).replace("-", "")
			post = Post.objects.filter(guid=post_guid).update(title=title, description=description,content=cont,author=string,visibility=visibility, pubDate=date, guid=guid)
		else:
			post = Posts(title=title,description=description,content=cont,author=string,visibility=visibility, pubDate=date, guid=guid)
		post.save()

		return HttpResponse(json.dumps({"posts" : title}))


def arefriends(request,authorguid1,authorguid2):
	f=Friends.objects.filter((Q(authorguid1=authorguid1)&Q(authorguid2=authorguid2)&Q(accepted=str(1)))|(Q(authorguid2=authorguid1)&Q(authorguid1=authorguid2)&Q(accepted=str(1))))
	if f:
		return HttpResponse("{\"query\": \"friends\"\"authors\": [\""+authorguid1+"\",\""+authorguid2+"\"], \"friends\": \"YES\" }:")
	else:
		return HttpResponse("{\"query\": \"friends\"\"authors\": [\""+authorguid1+"\",\""+authorguid2+"\"], \"friends\": \"NO\" }:")
def friends(request,authorguid1):
	lists=[]
	hi=json.loads(request.body)
	author=hi["author"]
	authors=hi["authors"]
	for author1 in authors:
		if Friends.objects.filter((Q(authorguid1=author)&Q(authorguid2=author1)&Q(accepted=str(1)))|(Q(authorguid2=author1)&Q(authorguid1=author)&Q(accepted=str(1)))):
			lists.append(author1)
	return HttpResponse(json.dumps({"friends":lists,"author":author,"query":"friends"}))
def friendrequest(request):
	hi=json.loads(request.body)
	author=hi["author"]["id"]
	authors=hi["friend"]["id"]
	if not Friends.objects.filter((Q(authorguid1=author)&Q(authorguid2=authors))|(Q(authorguid1=authors)&Q(authorguid2=author))):
		post_friend = Friends(authorguid1=author,authorguid2=authors, accepted=0)
		post_follow = Follows(authorguid1=author,authorguid2=authors)
		post_friend.save()
		post_follow.save()		
	return
