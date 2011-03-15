"""
Basic tests for system regression
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import Permission, User

from tvSite.guide.models import UserProfile, Show, GuideEntry

from datetime import datetime


class SimpleTest(TestCase):
    def setUp(self):
        """
        Required Setup for testing:
            -Create a user with permission to add favourites
            -Create a user with default premissions
            -Create a show with dummy data
            -Create blank user profile so favourites can be added
        """
        user = User.objects.create_user('john', 'someone@somewhere.com',
            'password')
        perm = Permission.objects.get(codename="can_have_favs")
        user.save()
        user.user_permissions.add(perm)
        profile = UserProfile()
        profile.user = user
        profile.save()

        user = User.objects.create_user('jane', 'someone@somewhere.com',
            'password')
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.save()

        new_show = Show()
        new_show.name = "Some test show"
        new_show.id = 1234
        new_show.save()

        new_entry = GuideEntry()
        #Compile a date/time stamp for the show
        date_object = datetime.strptime('2011-03-14 5:00 pm',
            '%Y-%m-%d %I:%M %p')
        new_entry.start = date_object
        new_entry.network = "SPIKE TV"
        new_entry.show = new_show
        new_entry.save()

    def test_main_page_anonymous(self):
        """
        Try to get the main page when not logged in
        """
        c = Client()
        response = c.get('/main/')
        self.failUnlessEqual(response.status_code, 200)

    def test_main_page_logged_in(self):
        """
        Try to get the main page when logged in
        """
        c = Client()
        self.failUnlessEqual(c.login(username='john', password='password'),
            True)
        response = c.get('/main/')
        self.failUnlessEqual(response.status_code, 200)

    def test_get_tv_listing_anonymous(self):
        """
        Try to get the tv guide when not logged in
        """
        c = Client()
        response = c.get('/main/tvjson/2011/3/14')
        self.failUnlessEqual(response.status_code, 200)

    def test_get_tv_listing_logged_in(self):
        """
        Try to get the tv guide when logged in
        """
        c = Client()
        self.failUnlessEqual(c.login(username='john', password='password'),
            True)
        response = c.get('/main/tvjson/2011/3/14')
        self.failUnlessEqual(response.status_code, 200)

    def test_toggle_fav_has_permission(self):
        """
        Toggle a favourite for the test user that has permissions
        """
        c = Client()
        self.failUnlessEqual(c.login(username='john', password='password'),
            True)
        response = c.post('/main/toggleFavShow/1234')
        #Status code 201 means it was created/added
        self.failUnlessEqual(response.status_code, 201)
        response = c.post('/main/toggleFavShow/1234')
        #Status code 200 means it was removed
        self.failUnlessEqual(response.status_code, 200)

    def test_toggle_fav_no_permission(self):
        """
        Toggle a favourite for the test user that does not have permissions
        """
        c = Client()
        self.failUnlessEqual(c.login(username='jane', password='password'),
            True)
        response = c.post('/main/toggleFavShow/1234')
        #Status code 302 means a redirect; to the login page
        self.failUnlessEqual(response.status_code, 302)
