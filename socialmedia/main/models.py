from django.db import models

class Post(models.Model):
	post = models.CharField(max_length=256)
	name = models.UsernameField(max_length=32)
	date = models.DateField(max_length=32)
	privacy = models.PrivacyField(max_length=32)
	extra = models.ExtraPrivacyField(max_length=32)

def __unicode__(self):
	return self.title

	
