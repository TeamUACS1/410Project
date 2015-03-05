from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Users

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
