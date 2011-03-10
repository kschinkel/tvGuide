from django.db import models
from django.contrib.auth.models import User

class StartTime(models.Model):
	start = models.DateTimeField()
	def __unicode__(self):
		return str(self.start)

class Show(models.Model):
	tID = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=200)
	start_times = models.ManyToManyField(StartTime)
	def __unicode__(self):
		return str(self.tID)+ ":" + self.name
	
class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	fav_shows = models.ManyToManyField(Show)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])