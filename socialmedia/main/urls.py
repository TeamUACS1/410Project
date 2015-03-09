from django.conf.urls import patterns, include, url
from main import views
urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^loggedin', views.showposts, name='showposts'),
url(r'^add_post/$', views.add_post, name='add_post'),
url(r'^seeAllPosts/$', views.seeAllPosts, name='seeAllPosts'),
url(r'^seefriendPosts/$', views.seeAllFriendPosts, name='seefriendPosts'),
url(r'^friendOfFriend/$', views.seeAllFoFPosts, name='seeAllFoFPosts'),
url(r'^main/signup', views.signup, name='signup'),
url(r'^main/login', views.login, name='login'),
url(r'^main/logout', views.logout, name='logout'),
url(r'^search', views.seeAllSearches, name='search'),
url(r'^addfriend', views.addFriend, name='addFriend'),
url(r'^delete/', views.delete, name='delete'),
url(r'^profile', views.profile, name='profile'),
)
