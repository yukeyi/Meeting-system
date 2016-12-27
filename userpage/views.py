from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import ConfBasic
from wechat.models import User
import urllib.request
import urllib.parse
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
        }
        print (result)
        return result


