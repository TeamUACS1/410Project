#main views file
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Q
import urllib2
import json
import uuid
from datetime import datetime
import hashlib
from main.models import Posts 
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows

#This function grabs the intital page after a user logs in. It brings up welcome.html
def index(request):
	context =RequestContext(request)
	request.session['logged_in']='f'
	request.session['user']=''
	request.session['admin']='f'
	return render_to_response('main/welcome.html',context)

#Showposts shows all the posts created by the author. It is displayed in the 'My Posts' section
def showposts(request):
	context =RequestContext(request)
	#author=Authors.objects.filter(displayname=request.session['user'])
	posts = Posts.objects.filter()
	return render_to_response('main/show_entries.html', {'posts': posts}, context)

#seeAllPosts shows all the public posts/ posts that the user has the right to view on the website. 
#Public posts have a flag of 0.
def seeAllPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.filter(Q(visibility='PUBLIC') | Q(author=user))
	return render_to_response('main/show_all_entries.html', {'posts': posts}, context)

#This function gets all the user's friends' posts and displays them on the window
def seeAllFriendPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.raw("select p.id from main_posts p, main_friends f where p.privateFlag = 2 and ((f.username2 = p.author and '" + user + "' = f.username1) or (f.username1 = p.author and '"+ user +"' = f.username2));")
	return render_to_response('main/show_friend_entries.html', {'posts': posts}, context)

#This function gets all the user's friends of friends' posts and displays them on the website
#Multiple SQL queries are used to gather the correct posts
def seeAllFoFPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	#grab ids and authors of posts that have a '4' friend of friend privacy flag
	authors = Posts.objects.raw("select distinct p.id, p.author from main_posts p, main_friends f where p.privateFlag = 4;")
	#grab all of people current user is friends with
	user_friend = Friends.objects.raw("select id, username1, username2 from main_friends where username1 = '" + user + "' or username2 = '"+ user +"'; ")
	total_posts = []
	looked_up = []
	looked_up.append(user)

	#loop through the objects to see if the post authors and current user have mutual friends. If so, display post. 
	for auth in authors:	
		for fid in user_friend:
			if(str(auth.author) not in looked_up):
				total = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username1) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username1) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				totalf = Friends.objects.raw("select count(*) from main_friends where ((f.username2 = '"+ str(fid.username2) +"' and '" + str(auth.author) + "' = f.username1) or (f.username1 = '"+ str(fid.username2) +"' and '"+ str(auth.author) +"' = f.username2)); ")	
				looked_up.append(str(auth.author))
				if (total or totalf):
					total_posts += Posts.objects.raw("select p.id from main_posts p where p.author = '"+ str(auth.author) +"'")
	return render_to_response('main/show_friend_of_friend.html', {'posts': total_posts}, context)

#Handles user login. Checks to see if login credentials are valid. Manages user and admin logins
def login(request):
	context =RequestContext(request)
	error =None
	if request.method=='POST':
		authors=Authors.objects.filter(displayname=request.POST.get("username", ""))
		password =request.POST.get("password", "")
		encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
		for author in authors:
			password=author.password
		if not authors:
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

#logs out a user
def logout(request):
	return redirect(index)

#Allows a user to sign up. It only allows for unique usernames in the database by checking against the db
def signup(request):
	context =RequestContext(request)
	session=request.session['logged_in']
	error =None
	host= "http://cs410.cs.ualberta.ca:41034"
	if request.method=='POST':
		displayname=request.POST.get("username", "")
		password=request.POST.get("password", "")
		authors=Authors.objects.filter(displayname=displayname)
		if authors:
			error='taken username'
		else:
			guid = uuid.uuid1()
			url = host+"/"+displayname+"/"+str(guid)
			password =request.POST.get("password", "")
			encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
			author=Authors(displayname=displayname,password=encrypted_pass, host=host, guid= guid, url=url, approved_flag=0)
			author.save()
			request.session['user']=request.POST.get("username", "")
			return render_to_response('main/signedup.html',{'error': error}, context)
	return render_to_response('main/signup.html',{'error': error}, context)

#Collects the information from a post sent by a logged in user
#If the flag is set to three you are sending a post to a specific user
#Save the post in the database making sure that the specified user can see it
"""def add_post(request):
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
	return redirect(showposts)"""

#Allows users to delete posts by passing the post's IDs and deleting it from the db
def delete(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		post =Posts(id=post)
		print (post)
		post.delete()
	return redirect(showposts)

#Allows users to edit a post and updating the existing post in the database
def edit(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		posts =Posts.objects.filter(id=post)
	return render_to_response('main/edit.html',{'posts': posts}, context)

#Is called after editing a posting and saving it
def save(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		title= request.POST.get("title", "")
		description= request.POST.get("description", "")
		cont= request.POST.get("post", "")
		flag = request.POST.get("privacy", "")
		date = datetime.now()
		post=Posts(id=post,title=title,description=description,content=cont,author=request.session['user'],privateFlag=flag,pubDate=date)
		post.save()
	return redirect(showposts)

#Collects the information from a post sent by a logged in user
#If the flag is set to three you are sending a post to a specific user
#Save the post in the database making sure that the specified user can see it
def add_post(request):
	context = RequestContext(request)
	date = datetime.now()
	if(request.method == 'POST'):
		title= request.POST.get("title", "")
		description= request.POST.get("description", "")
		cont= request.POST.get("post", "")
		visibility = request.POST.get("privacy", "")
		author = Authors(displayname=request.session['user'])
		author = author.displayname
		guid = uuid.uuid1()
		if(visibility == "3"):
			private_auth = request.POST.get("private_auth", "")
			post = Posts(title=title,description=description,content=cont,author=author,visibility="FOAF", pubDate=date, guid=guid)
		elif(visibility == "0"):
			post = Posts(title=title,description=description,content=cont,author=author,visibility="PUBLIC", pubDate=date, guid=guid)
		elif(visibility == "1"):
			post = Posts(title=title,description=description,content=cont,author=author,visibility="PRIVATE", pubDate=date, guid=guid)
		elif(visibility == "2"):
			post = Posts(title=title,description=description,content=cont,author=author,visibility="FRIEND", pubDate=date, guid=guid)
		elif(visibility == "4"):
			post = Posts(title=title,description=description,content=cont,author=author,visibility="SERVERONLY", pubDate=date, guid=guid)
		post.save()
	return redirect(showposts)

#Allows a user to add friends after finding another user to add.
#When this is called the adder becomes the addee's follower 
def addFriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		username2= request.POST.get("adduser", "")
		post_friend = Friends(username1=request.session['user'],username2=username2, followflag=0)
		post_friend.save()
	return redirect(seeAllSearches)

#Allows the user to search for other users using a specific username
def seeAllSearches(request):
	context =RequestContext(request)
	user= request.session['user']
	searchResult = ""
	if(request.method == 'POST'):
		username2 = request.POST.get("searchUser", "")
		searchResult = Users.objects.raw("select * from main_users where username='"+username2+"' and '"+username2+"' NOT IN (select username2 from main_friends where (username1 = '"+username2+"' and username2 = '"+user+"') or (username1 = '"+user+"' and username2 = '"+username2+"')) and '"+username2+"' NOT IN (select username1 from main_friends where (username1 = '"+username2+"' and username2 = '"+user+"') or (username1 = '"+user+"' and username2 = '"+username2+"'));")
	return render_to_response('main/search.html', {'searchResults': searchResult}, context)	

#This allows the user to change some of his profile settings and re encrypts the password if needed
#Lets the users change some settings and save them back to the db
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

#Display the current user's stream, posts and github activity
def myStream(request):
	context = RequestContext(request)
	error = None
	posts = Posts.objects.filter(privateFlag=0)
	current_user=request.session['user']
	user = Users.objects.get(username=current_user)

	posts = getGithubActivity(user)

	return render_to_response('main/myStream.html', {'posts': posts}, context)

#Fetches the github activity using the github api
def getGithubActivity(user):
	posts = ""
	if user.githubUsername:
		
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
			
			posts = activityList
		except urllib2.URLError, e:
			
			print("there was an error: %r" % e)

	return posts
