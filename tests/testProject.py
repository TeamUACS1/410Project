from django.test import TestCase
from django.test.client import Client
from main.models import Authors,Posts,Friends
from main.views import getGithubActivity

class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
	#self.response = self.client.post('/socialmedia/login', {'admin': 'admin', 'admin':'admin'})
	self.username1 = 'samohT'	
	self.github1 = 'curopium'
	self.user1 = Authors(displayname = self.username1)
	self.postText1 = "The quick brown fox jumps over the lazy dog"
	self.post1 = Posts(author = self.username1, content = self.postText1)
	self.username2 = 'ekiM'
	self.user2 = Authors(displayname = self.username2)
	#self.friends1 = Friends(username1 = self.username1, username2 = self.username2)

    def test_the_tests(self):
        self.assertEqual(True,True)

    def test_user_creation(self):
	self.assertEqual(self.user1.displayname,self.username1) 
	
    def test_post_creation(self):
        self.assertTrue((self.post1.author == self.username1) and (self.post1.content == self.postText1))
	
    #def test_friend_creation(self):
	#self.assertTrue((self.friends1.username1 == self.username1) and (self.friends1.username2 == self.username2))   

    #expected to not return anything because github name not set
    def test_github_githubUsernam_check(self):
	self.user1.github = ""
        self.assertEqual(getGithubActivity(self.user1), '')

    #will not work if you cant connect to github
    def test_github_activity_get(self):
	self.user1.github = self.github1
        self.assertTrue(getGithubActivity(self.user1))

    """
    def test_login(self):
        newresponse = self.client.post('/socialmedia/login', {'username': 'admin', 'password':'admin'}) 
	self.assertEquals(newresponse.status_code, 200)
	print("=-=-=-=-=-=-=-=-=")
	print(newresponse)
    """
