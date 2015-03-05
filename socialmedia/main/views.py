from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect

from main.models import Posts 
from main.models import Users



def index(request):
	context =RequestContext(request)
	request.session['logged_in']='f'
	session=request.session['logged_in']
	return render_to_response('main/welcome.html',context_instance=RequestContext(request, {'sessions':session,}))

def showposts(request):
	context =RequestContext(request)
	posts = Posts.objects.all()
	session=request.session['logged_in']
	return render_to_response('main/show_entries.html', {'posts': posts}, context_instance=RequestContext(request, {'sessions':session,}))

def login(request):
	context =RequestContext(request)
	session=request.session['logged_in']
	error =None
	if request.method=='POST':
		users=Users.objects.filter(username=request.POST.get("username", ""))
		encrypted_pass =request.POST.get("password", "")
		for user in users:
			password=user.password
		if not users:
			error='Not a used username'
		elif encrypted_pass!=password:
			error='Invalid Password'
		else:
			request.session['logged_in']="T"
			session=request.session['logged_in']
			print(request.session['logged_in'])
			print(session)
			return redirect(showposts)
	return render_to_response('main/login.html',{'error': error}, context_instance=RequestContext(request, {'sessions':session,}))



def signup():
	error =None
	if request.method=='POST':
		users=query_db('select * from users where username=?',		[request.form['username']])
		encrypted_pass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
	if not users:
		error='Not a used username'
	elif encrypted_pass!=users[0]['password']:
		error='Invalid Password'
	else:
		session['logged_in']=True
		return redirect(url_for('task'))
	return render_template('login.html',error=error)

def logout():
	error =None
	if request.method=='POST':
		users=query_db('select * from users where username=?',		[request.form['username']])
		encrypted_pass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
	if not users:
		error='Not a used username'
	elif encrypted_pass!=users[0]['password']:
		error='Invalid Password'
	else:
		session['logged_in']=True
		return redirect(url_for('task'))
	return render_template('login.html',error=error)

def add_post(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		postss = request.POST.get("post", "")

	# create and save link
		post =Posts(post=postss)
		post.save()
	# add tag to link
	return redirect(index)
