from django.conf.urls import patterns, include, url
from main import views
urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^loggedin', views.showposts, name='showposts'),
url(r'^add_post/$', views.add_post, name='add_post'),
<<<<<<< HEAD
url(r'^addPostUserProfile/$', views.addPostUserProfile, name='addPostUserProfile'),
url(r'^deletePostUserProfile/$', views.deletePostUserProfile, name='deletePostUserProfile'),
url(r'^seeAllPosts/$', views.seeAllPosts, name='seeAllPosts'),
=======
url(r'^seeAllPosts', views.seeAllPosts, name='seeAllPosts'),
>>>>>>> 82642e722f680f8a0614f5facf3c29433e829c5a
url(r'^seefriendPosts/$', views.seeAllFriendPosts, name='seefriendPosts'),
url(r'^friendOfFriend/$', views.seeAllFoFPosts, name='seeAllFoFPosts'),
url(r'^signup', views.signup, name='signup'),
url(r'^login', views.login, name='login'),
url(r'^logout', views.logout, name='logout'),
url(r'^search', views.seeAllSearches, name='search'),
url(r'^addfriend', views.addFriend, name='addFriend'),
url(r'^delete/', views.delete, name='delete'),
url(r'^save/', views.save, name='save'),
url(r'^edit/', views.edit, name='edit'),
url(r'^userProfile', views.userProfile, name='userProfile'),
url(r'^removeFriend/', views.removeFriend, name='removeFriend'),
url(r'^respondToFriendRequest/', views.respondToFriendRequest, name='respondToFriendRequest'),
url(r'^profileSettings', views.profileSettings, name='profileSettings'),
url(r'^myStream/$', views.myStream, name='myStream'),
)
