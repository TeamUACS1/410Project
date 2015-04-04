from django.test import TestCase
from django.test.client import Client
from main.models import Authors,Posts,Friends
from main.views import getGithubActivity

class ProjectTestCase(TestCase):
    """
    This file tests socialmedia's models and views, these are what
    makes the bulk of our project
    """
    def setUp(self):
        self.client = Client()
	self.username1 = 'samohT'
	self.guid1 = "id123"	
	self.github1 = 'curopium'
	self.user1 = Authors(displayname = self.username1, guid = self.guid1)
	self.postText1 = "The quick brown fox jumps over the lazy dog"
	self.post1 = Posts(author = self.username1, content = self.postText1)
	self.username2 = 'ekiM'
	self.guid2 = "otherid124"
	self.user2 = Authors(displayname = self.username2, guid= self.guid2)
	self.friends1 = Friends(authorguid1 = self.guid1,authorguid2 = self.guid2)

    def test_the_tests(self):
        """simply a test to make sure the tests are functional"""
        self.assertEqual(True,True)

    def test_user_creation(self):
        """Creates a user and checks to see if the name matches"""
	self.assertEqual(self.user1.displayname,self.username1) 
    def test_post_creation(self):
        """Creates a Post and checks to see if the content matches"""
        self.assertTrue((self.post1.author == self.username1) and (self.post1.content == self.postText1))
	
    def test_friend_creation(self):
        """Checks to see if the friend class has matching guids"""
	self.assertTrue((self.friends1.authorguid1 == self.guid1) and (self.friends1.authorguid2 == self.guid2))   

    #expected to not return anything because github name not set
    def test_github_githubUsernam_check(self):
        """This test to make sure that a none-existant github username dosent return anything"""
	self.user1.github = ""
        self.assertEqual(getGithubActivity(self.user1), '')

    def test_github_activity_get(self):
        """
	Test will fail if you cant connect to github.
	This test checks one of the team-members github account
        and returns any GitHub activity from that user. 
        """
	self.user1.github = self.github1
        self.assertTrue(getGithubActivity(self.user1))

