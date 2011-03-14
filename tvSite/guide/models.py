from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.id) + ": " + self.name

    class Meta:
        permissions = (
            ("can_have_favs", "Can the user have favourite shows"),
        )


class GuideEntry(models.Model):
    start = models.DateTimeField()
    network = models.CharField(max_length=25)
    show = models.ForeignKey(Show)
    def __unicode__(self):
        return str(str(self.start) + " "+ self.network + " " + str(self.show.id) + " " + self.show.name)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fav_shows = models.ManyToManyField(Show)
