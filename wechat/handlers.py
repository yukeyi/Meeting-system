# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import UserLogin, ConfBasic
import urllib.request
import urllib.parse
import json

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('您好，输入‘绑定’即可为您创建会佳账号并绑定微信。')



class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        openid = self.input['FromUserName']
        # 定义get的地址
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx9614f8da14f53590&secret=af4514adb134dd475588cd93c45ba790'
        # post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
        # 提交，发送数据
        req = urllib.request.Request(url)
        # 获取提交后返回的信息
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        re = json.loads(content)
        user_url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token='+re['access_token']+'&openid='+openid+'&lang=zh_CN'
        user_req = urllib.request.Request(user_url)
        user_response = urllib.request.urlopen(user_req)
        user_content = user_response.read().decode('utf-8')
        user_info = json.loads(user_content)
        print(user_info)
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            return self.reply_text('您已经绑定过了')
        else:
            data = {}
            data['nickname'] = str(user_info['nickname'])
            data['unionid'] = user_info['openid']
            data['headimgurl'] = user_info['headimgurl']
            data['sex'] = user_info['sex']
            data['location'] = user_info['country'] + user_info['province'] + user_info['city']
            data['language'] = user_info['language']
            print(data)
            hj_url = 'http://60.205.137.139/adminweb/REST/API-V2/loginToChinaByWeixin'
            hj_post = urllib.parse.urlencode(data).encode(encoding='utf-8')
            hj_req = urllib.request.Request(hj_url)
            hj_response = urllib.request.urlopen(hj_req, hj_post)
            hj_content = hj_response.read().decode('utf-8')
            hj_user_info = json.loads(hj_content)
            print(type(hj_user_info['data']['password']))
            createUser = UserLogin.objects.create(user_id=hj_user_info['data']['id'],
                                                  open_id=user_info['openid'],
                                                  email=hj_user_info['data']['email'])
            createUser.save()
            return self.reply_text('绑定成功！'+ '\n' +'您的会佳ID是' + str(hj_user_info['data']['id'])+';\n'+'您的密码是' + str(hj_user_info['data']['password']))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))
