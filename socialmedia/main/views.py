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

def index(request):
	context =RequestContext(request)
	request.session['logged_in']='f'
	request.session['user']=''
	request.session['admin']='f'
	return render_to_response('main/welcome.html',context)

def showposts(request):
	context =RequestContext(request)
	posts = Posts.objects.filter(author=request.session['user'])
	return render_to_response('main/show_entries.html', {'posts': posts}, context)

def showpostsUserProfile(request):
	context =RequestContext(request)
	posts = Posts.objects.filter(author=request.session['user'])
	session=request.session['logged_in']
	return posts
	#return render_to_response('main/userProfile.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.filter(Q(privateFlag=0) | Q(extra=user))
	return render_to_response('main/show_all_entries.html', {'posts': posts}, context)

def seeAllFriendPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.raw("select p.id from main_posts p, main_friends f where p.privateFlag = 2 and ((f.username2 = p.author and '" + user + "' = f.username1) or (f.username1 = p.author and '"+ user +"' = f.username2));")
	return render_to_response('main/show_friend_entries.html', {'posts': posts}, context)

def seeAllFoFPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	authors = Posts.objects.raw("select distinct p.id, p.author from main_posts p, main_friends f where p.privateFlag = 4;")
	user_friend = Friends.objects.raw("select id, username1, username2 from main_friends where username1 = '" + user + "' or username2 = '"+ user +"'; ")
	total_posts = []
	looked_up = []
	looked_up.append(user)

	for auth in authors:	
		for fid in user_friend:
			if(str(auth.author) not in looked_up):
				total = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username1) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username1) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				totalf = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username2) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username2) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				looked_up.append(str(auth.author))
				if (total or totalf):
					total_posts += Posts.objects.raw("select p.id from main_posts p where p.author = '"+ str(auth.author) +"'")
	return render_to_response('main/show_friend_of_friend.html', {'posts': total_posts}, context)

def login(request):
	context =RequestContext(request)
	error =None
	if request.method=='POST':
		users=Users.objects.filter(username=request.POST.get("username", ""))
		password =request.POST.get("password", "")
		encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
		for user in users:
			password=user.password
		if not users:
			error='Not a used username'
		elif encrypted_pass!=password:
			error='Invalid Password'
		else:
			request.session['logged_in']="T"
			session=request.session['logged_in']
			request.session['user']=request.POST.get("username", "")
			if request.POST.get("username", "")== "admin":
				request.session['admin']="T"
			return redirect(showposts)
	return render_to_response('main/login.html',{'error': error}, context)

def logout(request):
	return redirect(index)

def signup(request):
	context =RequestContext(request)
	session=request.session['logged_in']
	error =None
	if request.method=='POST':
		username=username=request.POST.get("username", "")
		password=request.POST.get("password", "")
		users=Users.objects.filter(username=request.POST.get("username", ""))
		if users:
			error='taken username'
		else:
			password =request.POST.get("password", "")
			encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
			user=Users(username=username,password=encrypted_pass, approved_flag=0)
			user.save()
			request.session['logged_in']="T"
			request.session['user']=request.POST.get("username", "")
			return render_to_response('main/signed.html',{'error': error}, context)
	return render_to_response('main/signedup.html',{'error': error}, context)


def add_post(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post2= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		if(flag == "3"):
			private_auth = request.POST.get("private_auth", "")
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag, extra=private_auth)
		else:
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag)
		post.save()
	return redirect(showposts)

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

def delete(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		post =Posts(id=post)
		post.delete()
	return redirect(showposts)


def edit(request):
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

def add_post(request):
	context = RequestContext(request)
	date = datetime.now()
	if(request.method == 'POST'):
		post2= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		if(flag == "3"):
			private_auth = request.POST.get("private_auth", "")
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag, extra=private_auth,date=date)
		else:
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag,date=date)
		post.save()
	return redirect(showposts)

def deletePostUserProfile(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("deleteID", "")
		post =Posts(id=post)
		post.delete()
	return redirect(userProfile)

def addFriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		username2= request.POST.get("adduser", "")
		post_friend = Friends(username1=request.session['user'],username2=username2, followflag=0)
		post_friend.save()
	return redirect(seeAllSearches)

def respondToFriendRequest(request):
	context = RequestContext(request)
	if (request.method == 'POST'):
		username2 = request.session['user']
		friendshipId = request.POST.get("requestUser", "")
		removeRequest = Friends.objects.filter(id = friendshipId).update(followflag=1)
	return redirect(userProfile)


def removeFriend(request):
	context = RequestContext(request)
	if (request.method == 'POST'):
		friendId= request.POST.get("IDS", "")
		friendInfo = Friends(id=friendId)
		friendInfo.delete()
	return redirect(userProfile)


def showFriendRequests(request):
	context = RequestContext(request)
	session = request.session['logged_in']
	user= request.session['user']
	requestList = Friends.objects.raw("select id, username1, username2, followflag from main_friends where followflag='0' and username2='" + user +"';")
	#return redirect()
	return requestList
	#return render_to_response('main/userProfile.html', {'requests': requestList}, context_instance=RequestContext(request, {'sessions':session,}))


def showUsersFollowing(request):
	context = RequestContext(request)
	session = request.session['logged_in']
	user= request.session['user']
	followingList = Friends.objects.raw("select id, username1, username2, followflag from main_friends where followflag='0' and username1='" + user +"';")
	return followingList
	#return render_to_response('main/userProfile.html', {'followers': followingList}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllSearches(request):
	context =RequestContext(request)
	searchResult = ""
	if(request.method == 'POST'):
		username2 = request.POST.get("searchUser", "")
		searchResult = Users.objects.filter(username=username2)
	return render_to_response('main/search.html', {'searchResults': searchResult}, context)	

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


def profileSettings(request):
	context =RequestContext(request)
	error = None
	
	if request.method=='POST':

		current_user=request.session['user']
		password = request.POST.get("newpassword","")
		githubUser = request.POST.get("githubname","")
		user = Users.objects.get(username=current_user)
		if password:
			encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
			user.password = encrypted_pass
			user.save()
		
		if githubUser:
			user.githubUsername = githubUser
			user.save()
	
	return render_to_response('main/profileSettings.html', {'error':error}, context)

def myStream(request):
	context = RequestContext(request)
	error = None
	posts = Posts.objects.filter(privateFlag=0)
	current_user=request.session['user']
	user = Users.objects.get(username=current_user)

	posts = getGithubActivity(user)

	return render_to_response('main/myStream.html', {'posts': posts}, context)


def getGithubActivity(user):
	posts = ""
	if user.githubUsername:
		#urlString = "http://api.github.com/users/" + user.githubUsername + "/events"
		activityList = []
		try:
			resp = urllib2.urlopen("https://api.github.com/users/"+user.githubUsername+"/events").read()
			jsonresp = json.loads(resp)
			#good tool for looking at the raw JSON: jsonformatter.curiousconcept.com
			for element in jsonresp:
				if element["type"] == "PushEvent":
					activityelem = ""
					activityelem += " At: "
					#date = ""
					date = element["created_at"]
					#TODO this is not working as intended
					date = date.replace('Z', '')
					date = date.replace('T', '')
					activityelem += date
					activityelem += " Pushed at repo: "
					activityelem += element["repo"]["name"]
					activityList.append(activityelem)	
			#print(activityList)
			posts = activityList
		except urllib2.URLError, e:
			#TODO handle this better
			print("there was an error: %r" % e)

	return posts
