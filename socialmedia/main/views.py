from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
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
	posts = Posts.objects.raw("select id from main_posts p, main_friends f where p.privateFlag = 2 and ((f.username2 = p.author and " + user +" = f.username1) or (f.username1 = p.author and "+ user +" = f.username2));")
	session=request.session['logged_in']
	return render_to_response('main/show_all_entries.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

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
		print flag
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


def changeGithub(request):
	context =RequestContext(request)
	#posts = Posts.objects.filter(author=request.session['user'])
	session=request.session['logged_in']
	error = None
	if request.method=='POST':
		#username=username.POST.get("username","")
		current_user=request.session['user']
		githubname = request.POST.get("githubname","")
		#user = Users.objects.filter(username=current_user)
		user = Users.objects.get(username=current_user)
		user.githubUsername = githubname
		user.save()
		

	return render_to_response('main/profile.html', {'error':error}, context_instance=RequestContext(request, {'sessions':session,}))

def delete(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		print post
		post =Posts(id=post)
		post.delete()
	return redirect(showposts)

