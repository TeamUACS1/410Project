import json,urllib2, base64
from django.test import TestCase


class APITestCases(TestCase):
    """Tests some of the API calls and there returns"""

    def setUp(self):
	self.url = "http://cmput410project15.herokuapp.com/main/"
	self.username = "user"
	self.password = "pass"


    def test_the_tests(self):
        """Simply a test to make sure the tests are functional"""
        self.assertEqual(True,True)

    def test_getposts(self):
        """tests to see if /getposts actually is returning posts"""
        request = urllib2.Request(self.url+"getposts/") 
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('/n','')
        request.add_header("Authorization", "Basic %s" % base64string)
        resultUrl = urllib2.urlopen(request)
        result = resultUrl.read()
        self.assertTrue(result)
