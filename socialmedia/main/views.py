from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect

from main.models import Posts 

def index(request):
	#Request the context of the request.
	#The context contains information such as the client's machine details for example.
	context =RequestContext(request)

	#Get all links

	posts = Posts.objects.all()
	return render_to_response('main/index.html', {'posts': posts}, context)

def tags(request):
	return render_to_response('main/index.html', {'posts': posts}, context)

def tag(request, tag_name):
	return render_to_response('main/index.html', {'posts': posts}, context)

def add_post(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		postss = request.POST.get("post", "")

	# create and save link
		post =Posts(post=postss)
		post.save()
	# add tag to link
	return redirect(index)
