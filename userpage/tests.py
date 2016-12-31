from django.core.urlresolvers import resolve
from django.test import TestCase
from wechat.models import User, Activity, Ticket, ConfBasic, UserLogin
from userpage.views import *
from userpage.urls import *
from django.contrib.auth.models import User as Superuser
from django.test import Client
import unittest
# Create your tests here.


class TestPostmessage(TestCase):
    def setUp(self):
        conf = ConfBasic.objects.create(
            conf_id = 1,
            name= 'a',
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
            price = 0,
        )
        conf.save()

    def test_correct_input(self):
        response = self.client.get('/api/u/message', {'id' :'1'})
        print(response.json())
        self.assertTrue(response.json()['data']['name'] == 'a')

    def test_lacking_input(self):
        response = self.client.get('/api/u/message')
        # print(response.json())
        self.assertEqual(response.json()['code'],1)

    def test_wrong_input(self):
        response = self.client.get('/api/u/message', {'id':'2'})
        #print(response.json())
        self.assertEqual(response.json()['code'],-1)



class TestpostJonConf(TestCase):
    def setUp(self):
        conf = ConfBasic.objects.create(
            conf_id=11,
            name='a',
            start_date='2016-11-11',
            end_date='2016-11-11',
            location='a',
            image='a',
            version=1,
            private_type=1,
            color='a',
            sequence='a',
            status=1,
            preview_code='a',
            zipcode='a',
            decs='a',
            poster='a',
            org='a',
            website='a',
            reg_url='a',
            phone='a',
            fax='a',
            email='a',
            wei_bo='a',
            wei_xin='a',
            qq='a',
            longitude='a',
            latitude='a',
            timezone='a',
            price = 0,
        )
        ulogin = UserLogin.objects.create(
            user_id=207,
            open_id='adagda',
            email='jhgfajgfaj',
            watching_page=1,
        )
        ulogin.save()
        conf.save()
    def test_correct_input(self):
        #response = self.client.get('/api/u/joinin', {'confid':'11'})
        response = self.client.get('/api/u/joinin', {'openid':'adagda', 'confid':'11'})
        #print(len(response.json()['data']))
        self.assertTrue(len(response.json()['data']) == 1)

    def test_wrong_input(self):
        response = self.client.get('/api/u/joinin', {'openid': 'adagda', 'confid': '111'})

        self.assertEqual(response.json()['code'], -1)

    def test_lacking_input(self):
        response = self.client.get('/api/u/joinin', {'openid': 'adagda'})

        self.assertEqual(response.json()['code'], 1)



class TestpostExitConf(TestCase):
    def setUp(self):
        conf = ConfBasic.objects.create(
            conf_id=11,
            name='a',
            start_date='2016-11-11',
            end_date='2016-11-11',
            location='a',
            image='a',
            version=1,
            private_type=1,
            color='a',
            sequence='a',
            status=1,
            preview_code='a',
            zipcode='a',
            decs='a',
            poster='a',
            org='a',
            website='a',
            reg_url='a',
            phone='a',
            fax='a',
            email='a',
            wei_bo='a',
            wei_xin='a',
            qq='a',
            longitude='a',
            latitude='a',
            timezone='a',
            price = 0,
        )
        ulogin = UserLogin.objects.create(
            user_id=207,
            open_id='adagda',
            email='jhgfajgfaj',
            watching_page=1,
        )
        ulogin.save()
        conf.save()

    def test_correct_input(self):
        response = self.client.get('/api/u/exit', {'openid': 'adagda', 'confid': '11'})
        print(response.json())
        self.assertEqual(response.json()['code'],0)

    def test_wrong_input(self):
        response = self.client.get('/api/u/exit', {'openid': 'adagda', 'confid': '111'})
        print(response.json())
        self.assertEqual(response.json()['code'], -1)

    def test_lacking_input(self):
        response = self.client.get('/api/u/exit', {'openid': 'adagda'})
        print(response.json())
        self.assertEqual(response.json()['code'], 1)

class TestMeetlist(TestCase):
    def setUp(self):
        conf = ConfBasic.objects.create(
            conf_id = 1,
            name= 'a',
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
            price = 0,
        )
        conf.save()

    def test_correct_result(self):
        response = self.client.get('/api/u/meetlist')
        self.assertEqual(len(response.json()['data']),1)


class TestPostmoney(TestCase):
    def setUp(self):
        conf = ConfBasic.objects.create(
            conf_id = 1,
            name= 'a',
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
            price = 0,
        )
        conf.save()

    def test_correct_input(self):
        response = self.client.get('/api/u/money', {'id': '1', 'money': '10'})
        self.assertEqual(response.json()['code'], 0)
        objs = ConfBasic.objects.all()
        self.assertEqual(objs[0].price, 10)

    def test_lacking_input(self):
        response = self.client.get('/api/u/money', {'id': '1'})
        self.assertEqual(response.json()['code'], 1)

    def test_wrong_input(self):
        response = self.client.get('/api/u/money', {'id': '111', 'money':'10'})
        self.assertEqual(response.json()['code'], -1)


class TestPosthome(TestCase):
    def test_correct_input(self):
        response = self.client.get('/api/u/home', {'id': '1'})
        self.assertEqual(response.json()['code'], 0)

    def test_lacking_input(self):
        response = self.client.get('/api/u/home')
        self.assertEqual(response.json()['code'], 1)