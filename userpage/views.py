from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import ConfBasic,UserLogin
from wechat.models import User
import urllib.request
import urllib.parse
import json
import requests
from django.http import HttpResponse

class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        self.check_input('openid')

        # 定义get的地址
        url = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        # post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
        headers = {'User-Agent': user_agent}
        # 提交，发送数据
        req = urllib.request.Request(url, headers)
        # 获取提交后返回的信息
        response = urllib.request.urlopen(req)
        content = response.geturl()
        return content

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()



class Postmessage(APIView):
    def get(self):
        self.check_input('id')
        print(self.input['id'])
        meet = ConfBasic.objects.get(conf_id=self.input['id'])
        result = {
            'id' : meet.conf_id,
            'name': meet.name,
            'image': meet.image,
            'start_date': str(meet.start_date),
            'end_date': str(meet.end_date),
            'location': meet.location,
            'version': meet.version,
            'privateType': meet.private_type,
            'sequence': meet.sequence,
            'status': meet.status,
            'desc': meet.decs,
            'website': meet.website,
            'phone': meet.phone,
            'fax': meet.fax,
            'email': meet.email,
        #    'address': ,
            'weibo': meet.wei_bo,
            'weixin': meet.wei_xin,
            'qq': meet.qq,
            'longtitude': meet.longitude,
            'latitude': meet.latitude,
            'timezone': meet.timezone,
            'price': meet.price,
        }
        print (result)
        return result

class postJoinConf(APIView):
    def get(self):
        self.check_input('confid','openid')
        data = {}
        temp = UserLogin.objects.filter(open_id=self.input['openid'])
        data['confid'] = self.input['confid']
        data['userid'] = temp[0].user_id
        data['type'] = 0
        hj_url = 'http://60.205.137.139/adminweb/REST/API-V2/joinConf'
        hj_post = urllib.parse.urlencode(data).encode(encoding='utf-8')
        hj_req = urllib.request.Request(hj_url)
        hj_response = urllib.request.urlopen(hj_req, hj_post)
        hj_content = hj_response.read().decode('utf-8')
        hj_info = json.loads(hj_content)

        conf = ConfBasic.objects.get(conf_id=self.input['confid'])
        temp[0].my_conf.add(conf)
        temp[0].save()
        return hj_info['data']

class postExitConf(APIView):
    def get(self):
        self.check_input('confid','openid')
        temp = UserLogin.objects.filter(open_id=self.input['openid'])
        data = {}
        data['confid'] = self.input['confid']
        data['userid'] = temp[0].user_id
        hj_url = 'http://60.205.137.139/adminweb/REST/API-V2/cancelConf'
        hj_post = urllib.parse.urlencode(data).encode(encoding='utf-8')
        hj_req = urllib.request.Request(hj_url)
        hj_response = urllib.request.urlopen(hj_req, hj_post)
        hj_content = hj_response.read().decode('utf-8')
        hj_info = json.loads(hj_content)

        conf = ConfBasic.objects.get(conf_id=self.input['confid'])
        temp[0].my_conf.remove(conf)
        temp[0].save()
        return hj_info['data']

class Posthome(APIView):
    def get(self):
        self.check_input('id')
        print(self.input['id'])
        get_access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx9614f8da14f53590&secret=af4514adb134dd475588cd93c45ba790"
        r = requests.get(get_access_token_url)
        access_token = r.json()['access_token']
        print(access_token)
        sendUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
        template_id = "nQRL9MRd-_ldZd9xV8hP8O-BFhkybSYL63vV8VzcZqg"
        for user in UserLogin.objects.all():
            if user.my_conf.all().filter(conf_id=self.input['id']):
                meetname = ConfBasic.objects.get(conf_id=self.input['id']).name
                message = '{"touser":"%(open_id)s","template_id":"%(template_id)s","url":"%(url)s","data":{"name":{"value":"%(conf_name)s"}}}' % {"open_id":user.open_id,"template_id":template_id,"url":"http://m2.huiplus.com.cn/app/#/confinfo/"+str(self.input['id']),"conf_name":meetname}
                message = message.encode('utf-8')
                reply = requests.post(sendUrl, data=message).json()
                print(user.user_id)
                print(reply)
        result = []
        return result

class Postmoney(APIView):
    def get(self):
        self.check_input('id','money')
        print(self.input['id'])
        conf = ConfBasic.objects.get(conf_id=self.input['id'])
        conf.price = self.input['money']
        conf.save()
        result = []
        return result

class Meetlist(APIView):
    def get(self):
        result = []
        conf = ConfBasic.objects.all()
        for i in conf:
            result.append((i.name,i.conf_id,i.price))
        return result



