from django.test import TestCase
import unittest
from django.contrib.auth.models import User as Admin
from wechat.models import User, Activity, Ticket, ConfBasic, UserLogin
from django.test import Client
import json
import time
import xml.etree.ElementTree as ET
# Create your tests here.

def createXML(openId, content):
    return '<xml><ToUserName><![CDATA[toUser]]></ToUserName><FromUserName><![CDATA['+openId+']]></FromUserName><CreateTime>'+str(int(time.time()))+'</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA['+content+']]></Content><MsgId>1</MsgId></xml>'

def createXMLButton(openId, event):
    return '<xml><ToUserName><![CDATA[toUser]]></ToUserName><FromUserName><![CDATA['+openId+']]></FromUserName><CreateTime>'+str(int(time.time()))+'</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[CLICK]]></Event><EventKey><![CDATA['+event+']]></EventKey><Content><![CDATA[抢票]]></Content><MsgId>1</MsgId></xml>'

def parse_msg_xml(response):
    elements = ET.fromstring(response.content)
    msg = dict()
    if elements.tag == 'xml':
        for child in elements:
            msg[child.tag] = child.text
    return msg

class TestMain(TestCase):

    def setUp(self):
        user1 = UserLogin.objects.create(open_id= 'qwertyuioplkjhgfdsazxcvbnm1',
                                         user_id= 207,
                                         email= '1@2.com',
                                         watching_page= 1)
        user2 = UserLogin.objects.create(open_id='qwertyuioplkjhgfdsazxcvbnm3',
                                         user_id=999,
                                         email='1@2.com',
                                         watching_page=1)

    def test_user_bind_text(self):
        c = Client()
        response = c.post('/wechat', data=createXML('qwertyuioplkjhgfdsazxcvbnm1','绑定'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:7], '您已经绑定过了')

        response = c.post('/wechat', data=createXML('o_fU2wQ7F8or2xptijjIZkDcCiSY','绑定'),content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:2], '绑定')

    def test_user_bind_menu(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'SERVICE_BIND'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:7], '您已经绑定过了')

        response = c.post('/wechat', data=createXMLButton('o_fU2wQ7F8or2xptijjIZkDcCiSY', 'SERVICE_BIND'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:2], '绑定')

    def test_all_meeting(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'ALL_MEETING'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'ALL_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['ArticleCount'], '4')

    def test_recent_meeting(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'RECENT_MEETING'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'RECENT_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['ArticleCount'], '1')

    def test_my_meeting(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'MY_MEETING'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm3', 'MY_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['Content'], '您没有关注或收藏的会议')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'MY_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertTrue(parse_msg_xml(response)['ArticleCount'] >= '0')

    def test_exit_meeting(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'EXIT_MEETING'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm3', 'EXIT_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['Content'], '您还没有加入任何会议')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'EXIT_MEETING'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertTrue(parse_msg_xml(response)['ArticleCount']>='0')

    def test_search_meeting(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'SEARCH_MEETING'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'SEARCH_MEETING'),
                          content_type='application/xml')
        # print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['Content'][:6], '请输入关键词')

        response = c.post('/wechat', data=createXML('qwertyuioplkjhgfdsazxcvbnm2','查询 刚到家啊果断'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXML('qwertyuioplkjhgfdsazxcvbnm1', '查询 刚到家啊果断'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:9], '没有查找到相关会议')

        response = c.post('/wechat', data=createXML('qwertyuioplkjhgfdsazxcvbnm1', '查询 会佳'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertTrue(parse_msg_xml(response)['ArticleCount']>='0')

    def test_quick_look(self):
        c = Client()
        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm2', 'QUICK_LOOK'),
                          content_type='application/xml')
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您还没进行过绑定')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm3', 'QUICK_LOOK'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['Content'], '您没有关注或收藏的会议')

        response = c.post('/wechat', data=createXMLButton('qwertyuioplkjhgfdsazxcvbnm1', 'QUICK_LOOK'),
                          content_type='application/xml')
        #print(parse_msg_xml(response))
        self.assertEqual(parse_msg_xml(response)['Content'][:8], '您的会议日程如下')