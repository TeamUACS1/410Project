from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
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
	session=request.session['logged_in']
	return render_to_response('main/welcome.html',context_instance=RequestContext(request, {'sessions':session,}))

def showposts(request):
	context =RequestContext(request)
	posts = Posts.objects.filter(author=request.session['user'])
	session=request.session['logged_in']
	return render_to_response('main/show_entries.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllPosts(request):
	context =RequestContext(request)
	posts = Posts.objects.filter(privateFlag=0)
	session=request.session['logged_in']
	return render_to_response('main/show_all_entries.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllFriendPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.raw("select p.id from main_posts p, main_friends f where p.privateFlag = 2 and ((f.username2 = p.author and '" + user + "' = f.username1) or (f.username1 = p.author and '"+ user +"' = f.username2));")
	session=request.session['logged_in']
	return render_to_response('main/show_friend_entries.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllFoFPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	authors = Posts.objects.raw("select distinct p.id, p.author from main_posts p, main_friends f where p.privateFlag = 4;")
	user_friend = Friends.objects.raw("select id, username1, username2 from main_friends where username1 = '" + user + "' or username2 = '"+ user +"'; ")
	total_posts = []
	looked_up = []
	looked_up.append(user)

	for auth in authors:
		if(str(auth.author) not in looked_up):
			for fid in user_friend:
				total = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username1) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username1) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				totalf = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username2) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username2) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				looked_up.append(str(auth.author))
				if (total or totalf):
					total_posts += Posts.objects.raw("select p.id from main_posts p where p.author = '"+ str(auth.author) +"'")

	session=request.session['logged_in']
	return render_to_response('main/show_friend_of_friend.html', {'posts': total_posts}, context_instance=RequestContext(request, {'sessions':session,}))

def login(request):
	context =RequestContext(request)
	session=request.session['logged_in']
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
			return redirect(showposts)
	return render_to_response('main/login.html',{'error': error}, context_instance=RequestContext(request, {'sessions':session,}))

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
			user=Users(username=username,password=encrypted_pass)
			user.save()
			request.session['logged_in']="T"
			session=request.session['logged_in']
			request.session['user']=request.POST.get("username", "")
			return redirect(showposts)
	return render_to_response('main/signup.html',{'error': error}, context_instance=RequestContext(request, {'sessions':session,}))


def add_post(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post2= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		if(flag == 3):
			#FASDF'SJDS'ADJF FIGURE IT OUT WHO USER IS
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag)
		else:
			post =Posts(post=post2,author=request.session['user'],privateFlag=flag)
		post.save()
	return redirect(showposts)


def addFriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		username2= request.POST.get("adduser", "")
		post_friend = Friends(username1=username2,username2=request.session['user'])
		post_friend.save()
	return redirect(seeAllSearches)

def showFriends(request):
	context =RequestContext(request)
	friendList = Friends.objects.filter(username1=request.session['user'])
	session=request.session['logged_in']
	return render_to_response('main/search.html', {'friends': friendList}, context_instance=RequestContext(request, {'sessions':session,}))

def seeAllSearches(request):
	context =RequestContext(request)
	searchResult = ""
	session = ""
	if(request.method == 'POST'):
		username2 = request.POST.get("searchUser", "")
		searchResult = Users.objects.filter(username=username2)
		session=request.session['logged_in']
	return render_to_response('main/search.html', {'searchResults': searchResult}, context_instance=RequestContext(request, {'sessions':session,}))	


def profile(request):
	context =RequestContext(request)
	#posts = Posts.objects.filter(author=request.session['user'])
	session=request.session['logged_in']
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
	
	return render_to_response('main/profile.html', {'error':error}, context_instance=RequestContext(request, {'sessions':session,}))


def myStream(request):
	context = RequestContext(request)
	session = request.session['logged_in']
	error = None
	posts = Posts.objects.filter(privateFlag=0)
	current_user=request.session['user']
	user = Users.objects.get(username=current_user)
	if user.githubUsername:
		#urlString = "http://api.github.com/users/" + user.githubUsername + "/events"
		urlString = "http://api.github.com/users/curopium/events"

		gitreq = urllib2.Request("http://api.github.com/users/curopium/events")
		#try:
		#	gitresp = urllib2.urlopen(gitreq)
		#except urllib2.URLError, e:
		#	raise MyException("there was an error: %r" % e)
		#posts = json.loads(gitresp.read())
		#print(posts)

	return render_to_response('main/myStream.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def delete(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		print post
		post =Posts(id=post)
		post.delete()
	return redirect(showposts)

