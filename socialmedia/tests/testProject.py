from django.test import TestCase
from django.test.client import Client
from main.models import Users,Posts

class ProjectTestCase(TestCase):
    def setUp(self):
	self.username1 = 'samohT'	
	self.user1 = Users(username = self.username1)
	self.postText1 = "The quick brown fox jumps over the lazy dog"
	self.post1 = Posts(author = self.username1, post = self.postText1)
    def test_the_tests(self):
        self.assertEqual(True,True)

    def test_user_creation(self):
        #user1 = Users(username = self.username1)
	self.assertEqual(self.user1.username,self.username1) 
	
    def test_post_creation(self):
        self.assertTrue((self.post1.author == self.username1) and (self.post1.post == self.postText1))
	
        
