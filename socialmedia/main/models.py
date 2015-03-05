from django.db import models

class Posts(models.Model):
	post = models.CharField(max_length=256)
	author = models.CharField(max_length=32)
	date = models.DateField(max_length=32)
	privateFlag = models.IntegerField(max_length=32)
	extra = models.CharField(max_length=32)

	def __unicode__(self):
		return self.author

class Users(models.Model):
	username = models.CharField(max_length=256, null=False)
	password = models.CharField(max_length=32)
	#image = models.ImageField(upload_to = 'images/profile_Img/')

class Friends(models.Model):
	username1=models.CharField(max_length=256, null=False)
	#username1=models.ForeignKey(Users, null=False)
	username2=models.CharField(max_length=256, null=False)
	#username2=models.ForeignKey(Users, null=False)
