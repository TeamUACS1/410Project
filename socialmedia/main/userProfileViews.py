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

def addPostUserProfile(request):
	context = RequestContext(request)
	session=request.session['logged_in']
	if(request.method == 'POST'):
		post2= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		if(flag == "3"):
			private_auth = request.POST.get("private_auth", "")
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag, extra=private_auth)
		else:
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag)
		post.save()
	return redirect(userProfile)
	#return render_to_response('main/userProfile.html', context_instance=RequestContext(request, {'sessions':session,}))

def deletePostUserProfile(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("deleteID", "")
		post =Posts(id=post)
		post.delete()
	return redirect(userProfile)

def removeFriend(request):
	context = RequestContext(request)
	if (request.method == 'POST'):
		friendId= request.POST.get("IDS", "")
		friendInfo = Friends(id=friendId)
		friendInfo.delete()
	return redirect(userProfile)

def respondToFriendRequest(request):
	context = RequestContext(request)
	if (request.method == 'POST'):
		username2 = request.session['user']
		friendshipId = request.POST.get("requestUser", "")
		removeRequest = Friends.objects.filter(id = friendshipId).update(followflag=1)
	return redirect(userProfile)


def showFriendRequests(request):
	context = RequestContext(request)
	session = request.session['logged_in']
	user= request.session['user']
	requestList = Friends.objects.raw("select id, username1, username2, followflag from main_friends where followflag=0 and username2='" + user +"';")
	#return redirect()
	return requestList
	#return render_to_response('main/userProfile.html', {'requests': requestList}, context_instance=RequestContext(request, {'sessions':session,}))

def showpostsUserProfile(request):
	context =RequestContext(request)
	posts = Posts.objects.filter(author=request.session['user'])
	session=request.session['logged_in']
	return posts
	#return render_to_response('main/userProfile.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def showUsersFollowing(request):
	context = RequestContext(request)
	session = request.session['logged_in']
	user= request.session['user']
	followingList = Friends.objects.raw("select id, username1, username2, followflag from main_friends where followflag=0 and username1='" + user +"';")
	return followingList
	#return render_to_response('main/userProfile.html', {'followers': followingList}, context_instance=RequestContext(request, {'sessions':session,}))

def userProfile(request):
	context = RequestContext(request)
	user = request.session['user']
	
	friendList = Friends.objects.raw("select id, username1, username2, followflag from main_friends where followflag=1 and (username1='" + user +"' or username2= '"+ user +"')")
	for friend in friendList:
		if friend.username1 != user:
			friend.username2 = friend.username1;
			friend.username1 = user;
	
	followingList = showUsersFollowing(request) 
	requestList = showFriendRequests(request)
	posts = showpostsUserProfile(request)
	return render_to_response('main/userProfile.html', {'friends': friendList, 'followers': followingList, 'requests': requestList, 'posts': posts}, context)
