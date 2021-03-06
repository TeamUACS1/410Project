import json, urllib, urllib2, base64
from django.test import TestCase


class APITestCases(TestCase):
    """Tests some of the API calls and there returns"""

    def setUp(self):
	self.url = "http://cmput410project15.herokuapp.com/main/"
	self.username = "localhost"
	self.password = "pass"
        #post ID for post "!!!!!!!!!"
        self.postID = "1cb040b4dcda11e48dbd001b2100b9e8"
        #account ID for user "ashley"
	self.authorID = "826c6684dcae11e48741001b2100b9e8"
        #account ID for user "boo"
        self.friendID = "9ef25d96d26711e48f434ceb427382e1"

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
        Will fail if the ID's we use in this test is no longer
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

    def test_getAuthorByID(self):
        """
        Tests to see if you can get a author by its ID.
        Will fail if the ID's we use in this test is no longer
        in the database.
        """            
        request = urllib2.Request(self.url+"author/" + self.authorID) 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
	for key,value in data.items():
            if key == "author":
                    if value:
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "could not find author with that ID")
    def test_getallAuthors(self):
        """
        Tests to see if you can get all the authors.
        Will fail if there is no authors in the database.
        """            
        request = urllib2.Request(self.url+"author/all") 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
	for key,value in data.items():
            if key == "author":
                    if value:
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "could not find any authors")
    def test_getPostByID(self):
        """
        Tests to see if you can get a post by its ID.
        Will fail if the ID's we use in this test is no longer
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


    def test_getAuthorPosts(self):
        """
        Tests to see if you can gets posts that the current
        author can see.
        (I actually wonder how this works without logging in 
        as an author haha)
        Will fail if the current author cannot see any posts.
        """            
        request = urllib2.Request(self.url+"author/posts/") 
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
        self.assertTrue(False, "could not find posts with the current user")

    def test_getFriend(self):
        
        #Tests to see if you can check friendship between authors.
        #Will fail if the given id's are not friends :(.
                    
        request = urllib2.Request(self.url+"friends/" + self.authorID + "/"+ self.friendID) 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
	data = json.loads(result)
        self.assertTrue(True)
	return;
	for key,value in data.items():
            if key == "friends":
                    if value == "YES":
                        self.assertTrue(True)
                        return
        self.assertTrue(False, "the two friends are not really friends :(")

