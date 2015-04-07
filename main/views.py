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
from django.core import serializers
from itertools import chain
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
			string=serializers.serialize("json",Authors.objects.filter(displayname=request.POST.get("username", "")),fields=('guid','host','displayname','url'))
			string=str(string).replace("fields","author")
			string=str(string).split("},")[0]
			string=string + "}}]"
			request.session['user']=string
			author=json.loads(string)
			request.session['user_json']=author[0]['author']
			authors=Authors.objects.filter(displayname=request.POST.get("username", ""))
			for author in authors:
				request.session['user_guid']=author.guid
				if request.POST.get("username", "")== "admin":
					request.session['admin']="T"
			return redirect(showposts)
	return render_to_response('main/login.html',{'error': error}, context)

#This function grabs the intital page after a user logs in. It brings up welcome.html
def index(request):
	context =RequestContext(request)
	request.session['logged_in']='f'
	request.session['user']=''
	request.session['friend_request']=''
	request.session['user_guid']=''
	request.session['admin']='f'
	request.session['friend']=''
	request.session['follow']=''
	return render_to_response('main/welcome.html',context)

#Showposts shows all the posts created by the author. It is displayed in the 'My Posts' section
def showposts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.filter(author=user)
	for post in posts:
		comments=Comments.objects.filter(post_guid=post.guid)
		setattr(post, 'comments', str(len(comments)))
		tempAuthor = json.loads(post.author)
		author = tempAuthor[0]['author']
		setattr(post, 'authorName', author['displayname'])
		setattr(post, 'authorGuid', author['guid'])
	posts = reversed(posts)
	return render_to_response('main/show_entries.html', {'posts':posts}, context)

#seeAllPosts shows all the public posts/ posts that the user has the right to view on the website. 
#Public posts have a flag of 0.
def seeAllPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.filter(Q(visibility='PUBLIC'))
	for post in posts:
		comments=Comments.objects.filter(post_guid=post.guid)
		setattr(post, 'comments', str(len(comments)))
		tempAuthor = json.loads(post.author)
		author = tempAuthor[0]['author']
		setattr(post, 'authorName', author['displayname'])
		setattr(post, 'authorGuid', author['guid'])
	posts = reversed(posts)
	return render_to_response('main/show_all_entries.html', {'posts': posts}, context)

#This function gets all the user's friends' posts and displays them on the window
def seeAllFriendPosts(request):
	context =RequestContext(request)
	user = request.session['user_guid']
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
	
		#posts.chain(posts, newpost)
		posts = posts | newpost
	
	for post in posts:
		comments=Comments.objects.filter(post_guid=post.guid)
		setattr(post, 'comments', str(len(comments)))
		tempAuthor = json.loads(post.author)
		author = tempAuthor[0]['author']
		setattr(post, 'authorName', author['displayname'])
		setattr(post, 'authorGuid', author['guid'])
	posts = reversed(posts)
	return render_to_response('main/show_friend_entries.html', {'posts': posts}, context)

#This function gets all the user's friends of friends' posts and displays them on the website
#Multiple SQL queries are used to gather the correct posts
def seeAllFoFPosts(request):
	context =RequestContext(request)
	user = request.session['user_guid']
	#grab ids and authors of posts that have a '4' friend of friend privacy flag
	authors = Posts.objects.raw("select distinct p.id, p.author from main_posts p, main_friends f where p.visibility ='FOAF';")
	#grab all of people current user is friends with
	user_friend = Friends.objects.raw("select id, authorguid1, authorguid2 from main_friends where authorguid1 = '" + user + "' or authorguid2 = '"+ user +"'; ")
	total_posts = []
	looked_up = []
	looked_up.append(user)

	#loop through the objects to see if the post authors and current user have mutual friends. If so, display post. 
	for auth in authors:	
		for fid in user_friend:
			if(str(auth.author) not in looked_up):
				total = Friends.objects.raw("select count(*) from main_friends where ((f.authorguid2 = '"+ str(fid.authorguid1) +"' and '" + str(auth.author) + "' = f.authorguid1) or (f.authorguid1 = '"+ str(fid.authorguid1) +"' and '"+ str(auth.author) +"' = f.authorguid2)); ")	
				totalf = Friends.objects.raw("select count(*) from main_friends where ((f.authorguid2 = '"+ str(fid.authorguid2) +"' and '" + str(auth.author) + "' = f.authorguid1) or (f.authorguid1 = '"+ str(fid.authorguid2) +"' and '"+ str(auth.author) +"' = f.authorguid2)); ")	
				looked_up.append(str(auth.author))
				if (total or totalf):
					total_posts += Posts.objects.raw("select p.id from main_posts p where p.author = '"+ str(auth.author) +"' and p.visibility ='FOAF';")
	for post in total_posts:
		comments=Comments.objects.filter(post_guid=post.guid)
		setattr(post, 'comments', str(len(comments)))
		tempAuthor = json.loads(post.author)
		author = tempAuthor[0]['author']
		setattr(post, 'authorName', author['displayname'])
		setattr(post, 'authorGuid', author['guid'])
	total_posts = reversed(total_posts)
	return render_to_response('main/show_friend_of_friend.html', {'posts': total_posts}, context)


#logs out a user
def logout(request):
	return redirect(index)

#Allows a user to sign up. It only allows for unique usernames in the database by checking against the db
def signup(request):
	context =RequestContext(request)
	session=request.session['logged_in']
	error =None
	host= "cmput410project15.herokuapp.com"
	if request.method=='POST':
		displayname=request.POST.get("username", "")
		password=request.POST.get("password", "")
		authors=Authors.objects.filter(displayname=displayname)
		if authors:
			error='taken username'
		else:
			guid = str(uuid.uuid1()).replace("-", "")
			url = host+"/main/author/"+str(guid)
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


#Allows users to delete posts by passing the post's IDs and deleting it from the db
def delete(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		post= request.POST.get("ID", "")
		post =Posts(id=post)
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
		visibility = request.POST.get("privacy", "")
		guid = request.POST.get("guid", "")

		date = datetime.now()
		author = request.session['user']
		post = Posts(id=post,title=title,description=description,content=cont,author=author,visibility=visibility, pubDate=date, guid=guid)
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
		author = request.session['user']

		guid = str(uuid.uuid1()).replace("-", "")
		post = Posts(title=title,description=description,content=cont,author=author,visibility=visibility, pubDate=date, guid=guid)
		post.save()
	return redirect(showposts)

def addComment(request):
	context = RequestContext(request)
	pubDate = datetime.now()
	if(request.method == 'POST'):
		comments= request.POST.get("comment", "")
		author_guid = request.session['user_guid']
		post_guid=request.POST.get("guid", "")
		guid = str(uuid.uuid1()).replace("-", "")
		comment = Comments(comments=comments,author_guid=author_guid,post_guid=post_guid, pubDate=pubDate, guid=guid)
		comment.save()
	return redirect(showposts)

#Allows a user to add friends after finding another user to add.
#When this is called the adder becomes the addee's follower 
def addFriend(request):
	context = RequestContext(request)
	if(request.method == 'POST'):
		username2= request.POST.get("ID", "")
		post_friend = Friends(authorguid1=request.session['user_guid'],authorguid2=username2, accepted=0)
		post_follow = Follows(authorguid1=request.session['user_guid'],authorguid2=username2)
		post_friend.save()
		post_follow.save()
	return redirect(seeAllSearches)

#Allows the user to search for other users using a specific username
def seeAllSearches(request):
	context =RequestContext(request)
	user= request.session['user']
	searchResult = ""
	allUsers = Authors.objects.raw("select * from main_authors")
	if(request.method == 'POST'):
		username = request.POST.get("searchUser", "")
		searchResult = Authors.objects.raw("select * from main_authors where displayname='"+username+"';")
	return render_to_response('main/search.html', {'searchResults': searchResult, 'allUsers': allUsers}, context)	



def viewfriend(request, author_guid):
	context = RequestContext(request)

	#This part gets you the user object for the profile page you are viewing
	userProfile = Authors.objects.filter(guid=author_guid)[0]

	#This part of code is for Pending Requests
	pendingRequests = Friends.objects.filter(Q(authorguid2=userProfile)&Q(accepted=str(0)))
	for pending in pendingRequests:
		setattr(pending, 'authorName', Authors.objects.filter(guid=pending.authorguid1)[0].displayname)

	#This part of code is for getting your friends
	friendsGuid=Friends.objects.filter((Q(authorguid1=author_guid)&Q(accepted=str(1)))|(Q(authorguid2=author_guid)&Q(accepted=str(1))))
	friends = []
	for friend in friendsGuid:
		if (friend.authorguid1 == author_guid):
			friends.append(Authors.objects.filter(guid=friend.authorguid2)[0])
		else:
			friends.append(Authors.objects.filter(guid=friend.authorguid1)[0])

	#This part of Code is for getting the Posts
	if (author_guid == request.session['user_guid']):
		posts=Posts.objects.filter(author=request.session['user'])
	else:
		posts=Posts.objects.filter(Q(visibility='PUBLIC'))
		temp = []
		for post in posts:
			author = json.loads(post.author)
			author = author[0]['author']
			if(author['guid'] == author_guid):
				temp.append(post)
		posts = temp

	return render_to_response('main/friend.html', {'friends': friends,"posts":posts, "userProfile": userProfile, "pendingRequests": pendingRequests}, context)

#This allows the user to change some of his profile settings and re encrypts the password if needed
#Lets the users change some settings and save them back to the db
def profileSettings(request):
	context =RequestContext(request)
	error = None
	
	if request.method=='POST':

		current_user=request.session['user_guid']
		password = request.POST.get("newpassword","")
		githubUser = request.POST.get("githubname","")
		user = Authors.objects.get(guid=current_user)
		if password:
			encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
			user.password = encrypted_pass
			user.save()
		
		if githubUser:
			user.github = githubUser
			user.save()
	
	return render_to_response('main/profileSettings.html', {'error':error}, context)

#This is where you get the details of a post.
def getpostdetails(request, post_guid):
	context = RequestContext(request)
	posts = Posts.objects.filter(guid=post_guid)
	comments=Comments.objects.filter(post_guid=post_guid)
	for post in posts:
		setattr(post, 'comments', str(len(comments)))
	for comment in comments:
		users = Authors.objects.get(guid=comment.author_guid)
		setattr(comment, 'author', users.displayname)
	return render_to_response('main/posts.html', {'posts':posts,'comments':comments}, context)
	

#Display the current user's stream, posts and github activity
def myStream(request):
	context = RequestContext(request)
	error = None
	current_user=request.session['user_guid']
	user = Authors.objects.get(guid=current_user)

	userPosts = Posts.objects.filter(Q(visibility='PUBLIC')| Q(author=user))
	githubPosts = getGithubActivity(user)

	postList = []
	#get each post title
        for post in userPosts:
            element =str(post.pubDate)+ " Posted: " + post.content 
            #element = post.title + post.description + post.content + str(post.pubDate) + post.author
            postList.append(element)

        #print(postList)
	posts =  postList + githubPosts
        posts.sort(reverse=True)

	return render_to_response('main/myStream.html', {'posts': posts}, context)

#Fetches the github activity using the github api
def getGithubActivity(user):
	posts = []
	if user.github:
		
		activityList = []
		try:
			resp = urllib2.urlopen("https://api.github.com/users/"+user.github+"/events").read()
			jsonresp = json.loads(resp)
			#good tool for looking at the raw JSON: jsonformatter.curiousconcept.com
			for element in jsonresp:
				if element["type"] == "PushEvent":
					activityelem = ""
					#activityelem += " At: "
					#date = ""
					date = element["created_at"]
					#TODO this is not working as intended
					date = date.replace('Z', ' ')
                                        date = date.split("T")[0]
					#date = date.replace('T', ' ')
					activityelem += date
					activityelem += " Pushed at repo: "
					activityelem += element["repo"]["name"]
					activityList.append(activityelem)	
			
			posts = activityList
		except urllib2.URLError, e:
			
			print("there was an error: %r" % e)

	return posts

def localCrossServerPosts(request):
	context =RequestContext(request)
	user = request.session['user']
	posts = Posts.objects.filter(Q(visibility='SERVERONLY'))
	for post in posts:
		tempAuthor = json.loads(post.author)
		author = tempAuthor[0]['author']
		setattr(post, 'authorName', author['displayname'])
		setattr(post, 'authorGuid', author['guid'])
	posts = reversed(posts)
	return render_to_response('main/localServerPosts.html', {'posts': posts}, context)
