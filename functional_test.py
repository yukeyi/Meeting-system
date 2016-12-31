from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os
import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from django.contrib.auth.models import User


def send_my_keys(obj, key):
    obj.clear()
    time.sleep(0.1)
    obj.send_keys(key)

class AdminLoginPageTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(AdminLoginPageTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username', '')
        cls.password = os.environ.get('password', '')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AdminLoginPageTest, cls).tearDownClass()

    def test_bind_user(self):
        #print(self.live_server_url)
        self.browser.get('http://183.172.97.125/AdminLogin.html')
        #self.browser.get_screenshot_as_file('1')
        name_box = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'name'))
        )
        name_box.send_keys('root')

        password_box = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'pass'))
        )
        password_box.send_keys('123') # 测试时补充正确密码
        #self.browser.get_screenshot_as_file('2')
        submit_button = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'btn'))
        )
        submit_button.click()
        time.sleep(1)
        #self.browser.get_screenshot_as_file('3')
        success_holder = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'head'))
         )
        #self.browser.get_screenshot_as_file('4')
        self.assertIn('觅听后台管理', success_holder.text)

class AdminTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(AdminTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username', '')
        cls.password = os.environ.get('password', '')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AdminTest, cls).tearDownClass()

    def test_propell(self):
        self.browser.get('http://183.172.97.125/home.html')
        self.browser.get_screenshot_as_file('1')
        submit_button = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'send11'))
        )
        submit_button.click()
        time.sleep(1)
        self.browser.get_screenshot_as_file('2')

    def test_changemoney(self):
        self.browser.get('http://183.172.97.125/home.html')
        self.browser.get_screenshot_as_file('1')
        money_box = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'money11'))
        )
        money_box.send_keys('10')
        submit_button = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'moneysend11'))
        )
        submit_button.click()
        time.sleep(1)
        self.browser.get_screenshot_as_file('2')
        self.browser.get('http://183.172.97.125/home.html')
        money_box = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'money11'))
        )
        self.assertIn('10', money_box.text)

class ExitTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(ExitTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username', '')
        cls.password = os.environ.get('password', '')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(ExitTest, cls).tearDownClass()

    def test_propell(self):
        self.browser.get('http://183.172.97.125/exit.html?1@o_fU2wUHF34t8fLxkTKFsv1BVtX4')
        self.browser.get_screenshot_as_file('1')
        submit_button = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'exitclick'))
        )
        submit_button.click()
        time.sleep(1)
        self.browser.get_screenshot_as_file('2')

class JoininTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(JoininTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username', '')
        cls.password = os.environ.get('password', '')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(JoininTest, cls).tearDownClass()

    def test_propell(self):
        self.browser.get('http://183.172.97.125/joinin.html?1@o_fU2wUHF34t8fLxkTKFsv1BVtX4')
        self.browser.get_screenshot_as_file('1')
        submit_button = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'joininclick'))
        )
        submit_button.click()
        time.sleep(1)
        self.browser.get_screenshot_as_file('2')
