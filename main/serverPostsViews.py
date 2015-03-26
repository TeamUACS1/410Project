from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import urllib2
import json
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows

def getPostsFromServers(request):
	context =RequestContext(request)
	url = 'http://thought-bubble.herokuapp.com/main/getposts/'
	serialized_data = urllib2.urlopen(url).read()
	data = json.loads(serialized_data)

	posts = []
	for key in data["posts"]:
		posts.append(key)
	#print data["posts"][0]["visability"]
		
	return render_to_response('main/show_other_server_posts.html', {'posts': posts}, context)
