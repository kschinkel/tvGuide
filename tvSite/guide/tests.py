"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import Permission

class SimpleTest(TestCase):
    def add_user(self):
        user = User.objects.create_user('john', 'someone@somewhere.com', 'password')
        perm = Permission.objects.get(codename="can_have_favs")
        user.save()
        user.user_permissions.add(perm)
        
    def test_main_page_logged_in(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.add_user()
        c = Client()
        self.failUnlessEqual(c.login(username='john', password='password'), True)
        response = c.get('/main/')
        self.failUnlessEqual(response.status_code, 200)
    def test_main_page_annon(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        c = Client()
        response = c.get('/main/')
        self.failUnlessEqual(response.status_code, 200)
    def test_add_fav_logged_in(self):
        self.add_user()
        c = Client()
        self.failUnlessEqual(c.login(username='john', password='password'), True)
        '''response = self.client.post(reverse('ajax_view'),
                            {'form':json_string}, 
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')'''
        print response.content
        self.failUnlessEqual(response.status_code, 200)
        
__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

