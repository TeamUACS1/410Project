from django.db import models

class Posts(models.Model):
	post = models.CharField(max_length=256)
	author = models.CharField(max_length=32)
	date = models.DateField(max_length=32)
	privateFlag = models.IntegerField(max_length=32)
	extra = models.CharField(max_length=32)

	def __unicode__(self):
		return self.title

	
