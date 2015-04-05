import json,urllib2, base64
from django.test import TestCase


class APITestCases(TestCase):
    """Tests some of the API calls and there returns"""

    def setUp(self):
	self.url = "http://cmput410project15.herokuapp.com/main/"
	self.username = "user"
	self.password = "pass"
        #post ID for post "!!!!!!!!!"
        self.postID = "03d3fa38d1bb11e4b41d4ceb427382e1"
        #account ID for user "ashley"
	self.authorID = "e76a5a0ed1ba11e4b1774ceb427382e1"

    def test_the_tests(self):
        """Simply a test to make sure the tests are functional"""
        self.assertEqual(True,True)

    def test_getPosts(self):
        """Tests to see if /getposts actually is returning posts."""
        request = urllib2.Request(self.url+"getposts/") 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
	for key,value in data.items():
            if key == "posts":
                    if value:
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "could not find any posts")

    def test_getPostByID(self):
        """
        Tests to see if you can get a post by its ID.
        Will fail if the id we use in this test is no longer
        in the database.
        """            
        request = urllib2.Request(self.url+"posts/" + self.postID) 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
	for key,value in data.items():
            if key == "posts":
                    if value:
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "could not find post with that id")

    def test_getPostByAuthorID(self):
        """
        Tests to see if you can get a post by its ID.
        Will fail if the id we use in this test is no longer
        in the database.
        """            
        request = urllib2.Request(self.url+"author/" + self.authorID + "/posts/") 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
	for key,value in data.items():
            if key == "posts":
                    if value:
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "could not find any posts from this author ID. ")
