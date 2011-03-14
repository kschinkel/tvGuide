from django.db import models
from django.contrib.auth.models import User


class StartTime(models.Model):
    start = models.DateTimeField(primary_key=True)

    def __unicode__(self):
        return str(self.start)


class Show(models.Model):
    name = models.CharField(max_length=200)
    start_times = models.ManyToManyField(StartTime)

    def __unicode__(self):
        return str(self.id) + ":" + self.name

    class Meta:
        permissions = (
            ("can_have_favs", "Can the user have favourite shows"),
        )


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fav_shows = models.ManyToManyField(Show)
