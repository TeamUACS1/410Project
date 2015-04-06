from django.conf.urls import patterns, include, url
from main import views
from main import adminviews
from main import apiviews
from main import userProfileViews
from main import serverViews
urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^loggedin', views.showposts, name='showposts'),
url(r'^add_post/$', views.add_post, name='add_post'),
url(r'^addPostUserProfile/$', userProfileViews.addPostUserProfile, name='addPostUserProfile'),
url(r'^deletePostUserProfile/$', userProfileViews.deletePostUserProfile, name='deletePostUserProfile'),
url(r'^seeAllPosts/$', views.seeAllPosts, name='seeAllPosts'),
url(r'^seefriendPosts/$', views.seeAllFriendPosts, name='seefriendPosts'),
url(r'^friendOfFriend/$', views.seeAllFoFPosts, name='seeAllFoFPosts'),
url(r'^localCrossServerPosts/$', views.localCrossServerPosts, name='localCrossServerPosts'),
url(r'^signup', views.signup, name='signup'),
url(r'^login', views.login, name='login'),
url(r'^logout', views.logout, name='logout'),
url(r'^search', views.seeAllSearches, name='search'),
url(r'^addfriend', views.addFriend, name='addFriend'),
url(r'^author/(?P<author_guid>\w+)/feed', views.viewfriend, name='viewFriend'),
url(r'^delete/', views.delete, name='delete'),
url(r'^save/', views.save, name='save'),
url(r'^edit/', views.edit, name='edit'),
url(r'^userProfile', userProfileViews.userProfile, name='userProfile'),
url(r'^removeFriend/', userProfileViews.removeFriend, name='removeFriend'),
url(r'^respondToFriendRequest/', userProfileViews.respondToFriendRequest, name='respondToFriendRequest'),
url(r'^profileSettings', views.profileSettings, name='profileSettings'),
url(r'^myStream/$', views.myStream, name='myStream'),
url(r'^otherServerPost/$', serverViews.getPostsFromServers, name='getPostsFromServers'),
url(r'^otherServerAuthors', serverViews.getallauthors, name='getallauthors'),
url(r'^othernodePostId/$', serverViews.searchPostId, name='othernodePostId'),
url(r'^specificauthorposts/$', serverViews.specificauthorposts, name='specificauthorposts'),
url(r'^currentlyauthuser/$', serverViews.currentlyauthuser, name='currentlyauthuser'),
url(r'^friendcheck/$', serverViews.iffriend, name='iffriend'),
url(r'^friendreq/$', serverViews.friendreq, name='friendreq'),
url(r'^foaf/$', serverViews.getpostifFOAF, name='getpostifFOAF'),
url(r'^approveAuthors/$', adminviews.approveAuthor, name='approveAuthor'),
url(r'^manageAuthors/$', adminviews.manageAuthor, name='manageAuthor'),
url(r'^approve/$', adminviews.approve, name='approve'),
url(r'^deleteauthor/$', adminviews.deleteauthor, name='deleteauthor'),
url(r'^editauthor/$', adminviews.editauthor, name='editauthor'),
url(r'^saveauthor/$', adminviews.saveauthor, name='saveauthor'),
url(r'^getposts', apiviews.getposts, name='getposts'),
url(r'^author/posts', apiviews.authorposts, name='authorposts'),
url(r'^author/(?P<author_guid>\w+)/posts', apiviews.authorsposts, name='vauthorsposts'),
url(r'^posts/(?P<post_guid>\w+)', apiviews.getpost, name='getpost'),
url(r'^friends/(?P<authorguid1>\w+)/(?P<authorguid2>\w+)', apiviews.arefriends, name='arefriends'),
url(r'^friends/(?P<authorguid1>\w+)', apiviews.friends, name='friends'),
url(r'^friendrequest', apiviews.friendrequest, name='friendrequest'),
url(r'^author/(?P<authorguid1>\w+)', apiviews.getspecificauthors, name='getspecificauthors'),
url(r'^seepostdetails/(?P<post_guid>\w+)',views.getpostdetails,name='getpostdetails'),
url(r'^add_comment/',views.addComment,name='addComment'),
url(r'^approveHosts', adminviews.approveHosts, name='approveHosts'),
url(r'^manageHosts', adminviews.manageHosts, name='manageHosts'),
url(r'^addHosts', adminviews.addHosts, name='addHosts'),


)
