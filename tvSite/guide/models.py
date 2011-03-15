from django.db import models
from django.contrib.auth.models import User


class Show(models.Model):
    """
    This class contains the name of the show
    as well as the id.
    The id is not defined here as it is added
    by default to every model
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.id) + ": " + self.name

    class Meta:
        """
        Add the necessary permissions for the show model
        """
        permissions = (
            ("can_have_favs", "Can the user have favourite shows"),
        )


class GuideEntry(models.Model):
    """
    This class contains the start time,
    network that it is playing on, and
    a referance to a show
    """
    start = models.DateTimeField()
    network = models.CharField(max_length=25)
    show = models.ForeignKey(Show)

    def __unicode__(self):
        return str(str(self.start) + " " + self.network + " "
            + str(self.show.id) + " " + self.show.name)


class UserProfile(models.Model):
    """
    This class 'extends' the user model
    so that favourites can be linked to a user
    """
    user = models.ForeignKey(User, unique=True)
    fav_shows = models.ManyToManyField(Show)
