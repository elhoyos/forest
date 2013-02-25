from django.test import TestCase
from django.test.client import Client
from forest.main.models import Stand
from django.contrib.auth.models import User, Group


class SimpleTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="testuser")
        self.g = Group.objects.create(name="testgroup")
        self.u.groups.add(self.g)
        self.stand = Stand.objects.create(
            title="test stand",
            hostname="test.example.com",
            access="open",
        )
        self.c = Client()

    def tearDown(self):
        self.g.delete()
        self.u.delete()

    def test_index(self):
        response = self.c.get('/', HTTP_HOST="test.example.com")
        self.assertEquals(response.status_code, 302)

    def test_smoketests(self):
        # just request them to make sure they are covered
        # it's actually ok for the smoketests to return a "FAIL"
        # we don't care about that here. We just want to know
        # that the smoketests are runnable and not erroring out
        # themselves
        response = self.c.get('/smoketest/')
        self.assertEquals(response.status_code, 200)

    def test_css(self):
        response = self.c.get('/_stand/css/', HTTP_HOST="test.example.com")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], "text/css")