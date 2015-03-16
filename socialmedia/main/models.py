from django.db import models

class Posts(models.Model):
	title = models.CharField(max_length=100)
	source = models.CharField(max_length=256)
	origin = models.CharField(max_length=256)
	description = models.CharField(max_length=256)
	content_type = models.CharField(max_length=256)
	content = models.CharField(max_length=512)
	author = models.ManyToManyField(Authors)
	categories = models.CharField(max_length=32)
	comments = models.ManyToManyField(Comments)
	pubDate = models.DateField(max_length=32)
	visibility = models.CharField(max_length=16)
	guid = models.CharField(max_length=32)

	def __unicode__(self):
		return self.author
	

class Authors(models.Model):
	host = models.CharField(max_length=32, null=False)
	displayname = models.CharField(max_length=32, null=False)
	password = models.CharField(max_length=32, null=False)
	github = models.CharField(max_length=40)
	approved_flag=models.IntegerField(max_length=8)
	url = models.CharField(max_length=257)
	guid = models.CharField(max_length=32)


class Comments(models.Model):
	author = models.CharField(max_length=32, null=False)
	comments = models.CharField(max_length=512)
	pubDate = models.DateField(max_length=32)
	guid = models.CharField(max_length=32)


class Friends(models.Model):
	authorguid1=models.CharField(max_length=32, null=False)
	authorguid2=models.CharField(max_length=32, null=False)
	accepted = models.CharField(max_length=8, null=False)
	
class Follows(models.Model):
	authorguid1=models.CharField(max_length=32, null=False)
	authorguid2=models.CharField(max_length=32, null=False)

























