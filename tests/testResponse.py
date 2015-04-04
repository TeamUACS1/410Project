# run python freetests.py while server is running

import urllib2
import unittest

BASEURL = "http://127.0.0.1:8000"

class TestYourWebserver(unittest.TestCase):
    """
    Tests some the responses from the server with urllib2
    """
    def setUp(self,baseurl=BASEURL):
        self.baseurl = baseurl

    def test_get_indexhtml(self):
        """Tests to see if we can get 200 OK from the mainpage"""
        url = self.baseurl + "/main"
        req = urllib2.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")

    def test_get_404(self):
        """This tests for a 404 error for a page that dosent exist"""
        url = self.baseurl + "/do-not-implement-this-page-it-is-not-found"
        try:
            req = urllib2.urlopen(url, None, 3)
            self.assertTrue( False, "Should have thrown an HTTP Error!")
        except urllib2.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , ("404 Not FOUND! %d" % e.getcode()))
        else:
            self.assertTrue( False, "Another Error was thrown!")
        
if __name__ == '__main__':
    unittest.main()

