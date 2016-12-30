from django.test import TestCase
from wechat.models import User, Activity, Ticket, ConfBasic, UserLogin
from userpage.views import *
from django.contrib.auth.models import User as Superuser
from django.test import Client
import unittest
# Create your tests here.

class TestPostmessage(TestCase):

    def setup(self):
        conf = ConfBasic.objects.create(
            conf_id = 123,
            name='a',
            start_date = '2016-11-11',
            end_date = '2016-11-11',
            location = 'a',
            image = 'a',
            version = 1,
            private_type = 1,
            color = 'a',
            sequence = 'a',
            status = 1,
            preview_code = 'a',
            zipcode = 'a',
            decs = 'a',
            poster = 'a',
            org = 'a',
            website = 'a',
            reg_url = 'a',
            phone = 'a',
            fax = 'a',
            email = 'a',
            wei_bo = 'a',
            wei_xin = 'a',
            qq = 'a',
            longitude = 'a',
            latitude = 'a',
            timezone = 'a',
        )
        conf.save()

    def correct_input(self):
        response = self.client.get('/api/u/message', {'id' :1})
        # print(response.json())
        self.assertTrue(len(response.json()['data']) == 1)
