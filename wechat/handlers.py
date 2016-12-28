# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import UserLogin, ConfBasic
import urllib.request
import urllib.parse
import json

__author__ = "Epsirom"

def AddHeader(path):
    return ("http://183.172.98.130/"+ path)

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
        #print(user_info)
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
            #print(data)
            hj_url = 'http://60.205.137.139/adminweb/REST/API-V2/loginToChinaByWeixin'
            hj_post = urllib.parse.urlencode(data).encode(encoding='utf-8')
            hj_req = urllib.request.Request(hj_url)
            hj_response = urllib.request.urlopen(hj_req, hj_post)
            hj_content = hj_response.read().decode('utf-8')
            hj_user_info = json.loads(hj_content)
            #print(type(hj_user_info['data']['password']))
            createUser = UserLogin.objects.create(user_id=hj_user_info['data']['id'],
                                                  open_id=user_info['openid'],
                                                  email=hj_user_info['data']['email'])
            createUser.save()
            return self.reply_text('绑定成功！'+ '\n' +'您的会佳ID是' + str(hj_user_info['data']['id'])+';\n'+'您的密码是' + str(hj_user_info['data']['password']))


class AllMeetingsHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['all_meeting'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            print(temp[0].watching_page)
            url = 'http://60.205.137.139/adminweb/REST/API-V2/allConfList?userid='+str(temp[0].user_id)+'&page='+str(temp[0].watching_page)+'&page_size='+str(3)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)
            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                print(mesre['data']['basic']['name'])
                #print(mesre)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data']['basic']['id'],
                        name = mesre['data']['basic']['name'],
                        start_date = mesre['data']['basic']['startDate'],
                        end_date = mesre['data']['basic']['endDate'],
                        #logo = mesre['data']['logo'],
                        location = mesre['data']['basic']['location'],
                        image = mesre['data']['basic']['image'],
                        version = mesre['data']['basic']['version'],
                        #private = mesre['data']['basic']['isPrivate'],
                        private_type = mesre['data']['detail']['privateType'],
                        sequence = mesre['data']['basic']['sequence'],
                        status = mesre['data']['basic']['status'],
                        decs = mesre['data']['detail']['desc'],
                        website = mesre['data']['detail']['website'],
                        phone = mesre['data']['detail']['phone'],
                        fax = mesre['data']['detail']['fax'],
                        email = mesre['data']['detail']['email'],
                        wei_bo = mesre['data']['detail']['weibo'],
                        wei_xin = mesre['data']['detail']['weixin'],
                        qq = mesre['data']['detail']['qq'],
                        longitude = mesre['data']['detail']['longitude'],
                        latitude = mesre['data']['detail']['latitude'],
                        timezone = mesre['data']['detail']['timeZone'],
                    )
                    createActivity.save()







            if len(re['data']) == 0:
                return self.reply_text("目前没有会议")
           # print(re['data'])
            pagenumber = temp[0].watching_page
            if temp[0].watching_page * 3 > re['total_size']:
                temp[0].watching_page = 1
                temp[0].save()
            else:
                temp[0].watching_page = temp[0].watching_page + 1
                temp[0].save()

            ans = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:15]+"..."
                else:
                    name = re['data'][index]['name']
                print(temp[0].my_conf.all())
                if (temp[0].my_conf.all().filter(conf_id=re['data'][index]['id'])):
                    url = 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(re['data'][index]['id'])
                else:
                    url = AddHeader('message.html?'+str(re['data'][index]['id'])+ '@' +str(temp[0].user_id))
                ans.append({
                    'Title': name,
                    'Url': url,
                    'PicUrl': 'http://60.205.137.139/adminweb/'+ re['data'][index]['image'],
                })
            ans.append({'Title' : '再次点击所有会议查看更多 当前页面：'+ str(pagenumber)})
            return self.reply_news(ans)
        else:
            return self.reply_text("您还没进行过绑定")


class RecentMeetingHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['recent'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/upcomingConfList?userid='+str(temp[0].user_id)+'&page='+str(1)+'&page_size='+str(10)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)

            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data'][index]['id'],
                        name = mesre['data'][index]['name'],
                        start_date = mesre['data'][index]['start_date'],
                        end_date = mesre['data'][index]['end_date'],
                        logo = mesre['data'][index]['logo'],
                        location = mesre['data'][index]['location'],
                        image = mesre['data'][index]['image'],
                        version = mesre['data'][index]['version'],
                        private = mesre['data'][index]['private'],
                        private_type = mesre['data'][index]['privateType'],
                        sequence = mesre['data'][index]['sequence'],
                        status = mesre['data'][index]['status'],
                        desc = mesre['data'][index]['detail']['desc'],
                        website = mesre['data'][index]['detail']['website'],
                        phone = mesre['data'][index]['detail']['phone'],
                        fax = mesre['data'][index]['detail']['fax'],
                        email = mesre['data'][index]['detail']['email'],
                        wei_bo = mesre['data'][index]['detail']['weibo'],
                        wei_xin = mesre['data'][index]['detail']['weixin'],
                        qq = mesre['data'][index]['detail']['qq'],
                        longtitude = mesre['data'][index]['detail']['longtitude'],
                        latitude = mesre['data'][index]['detail']['latitude'],
                        timezone = mesre['data'][index]['detail']['timeZone'],
                    )
                    createActivity.save()



            if len(re['data']) == 0:
                return self.reply_text("近期没有会议")

            ans = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:15]+"..."
                else:
                    name = re['data'][index]['name']
                if (temp[0].my_conf.all().filter(conf_id=re['data'][index]['id'])):
                    url = 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(re['data'][index]['id'])
                else:
                    url = AddHeader('message.html?'+str(re['data'][index]['id'])+ '@' +str(temp[0].user_id))
                ans.append({
                    'Title': name,
                    'Url': url,
                    'PicUrl': 'http://60.205.137.139/adminweb/'+ re['data'][index]['image'],
                })
            return self.reply_news(ans)
        else:
            return self.reply_text("您还没进行过绑定")

class MyMeetingHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['my_meeting'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid='+str(temp[0].user_id)+'&page='+str(1)+'&page_size='+str(3)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)

            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data'][index]['id'],
                        name = mesre['data'][index]['name'],
                        start_date = mesre['data'][index]['start_date'],
                        end_date = mesre['data'][index]['end_date'],
                        logo = mesre['data'][index]['logo'],
                        location = mesre['data'][index]['location'],
                        image = mesre['data'][index]['image'],
                        version = mesre['data'][index]['version'],
                        private = mesre['data'][index]['private'],
                        private_type = mesre['data'][index]['privateType'],
                        sequence = mesre['data'][index]['sequence'],
                        status = mesre['data'][index]['status'],
                        desc = mesre['data'][index]['detail']['desc'],
                        website = mesre['data'][index]['detail']['website'],
                        phone = mesre['data'][index]['detail']['phone'],
                        fax = mesre['data'][index]['detail']['fax'],
                        email = mesre['data'][index]['detail']['email'],
                        wei_bo = mesre['data'][index]['detail']['weibo'],
                        wei_xin = mesre['data'][index]['detail']['weixin'],
                        qq = mesre['data'][index]['detail']['qq'],
                        longtitude = mesre['data'][index]['detail']['longtitude'],
                        latitude = mesre['data'][index]['detail']['latitude'],
                        timezone = mesre['data'][index]['detail']['timeZone'],
                    )
                    createActivity.save()




            if len(re['data']) == 0:
                return self.reply_text("您没有关注或收藏的会议")

            ans = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:15]+"..."
                else:
                    name = re['data'][index]['name']
                if (temp[0].my_conf.all().filter(conf_id=re['data'][index]['id'])):
                    url = 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(re['data'][index]['id'])
                else:
                    url = AddHeader('message.html?'+str(re['data'][index]['id'])+ '@' +str(temp[0].user_id))
                ans.append({
                    'Title': name,
                    'Url': url,
                    'PicUrl': 'http://60.205.137.139/adminweb/'+ re['data'][index]['image'],
                })
            return self.reply_news(ans)
        else:
            return self.reply_text("您还没进行过绑定")

class ExitMeetingHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['exit_meeting'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid='+str(temp[0].user_id)+'&page='+str(1)+'&page_size='+str(3)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)

            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data'][index]['id'],
                        name = mesre['data'][index]['name'],
                        start_date = mesre['data'][index]['start_date'],
                        end_date = mesre['data'][index]['end_date'],
                        logo = mesre['data'][index]['logo'],
                        location = mesre['data'][index]['location'],
                        image = mesre['data'][index]['image'],
                        version = mesre['data'][index]['version'],
                        private = mesre['data'][index]['private'],
                        private_type = mesre['data'][index]['privateType'],
                        sequence = mesre['data'][index]['sequence'],
                        status = mesre['data'][index]['status'],
                        desc = mesre['data'][index]['detail']['desc'],
                        website = mesre['data'][index]['detail']['website'],
                        phone = mesre['data'][index]['detail']['phone'],
                        fax = mesre['data'][index]['detail']['fax'],
                        email = mesre['data'][index]['detail']['email'],
                        wei_bo = mesre['data'][index]['detail']['weibo'],
                        wei_xin = mesre['data'][index]['detail']['weixin'],
                        qq = mesre['data'][index]['detail']['qq'],
                        longtitude = mesre['data'][index]['detail']['longtitude'],
                        latitude = mesre['data'][index]['detail']['latitude'],
                        timezone = mesre['data'][index]['detail']['timeZone'],
                    )
                    createActivity.save()




            if len(re['data']) == 0:
                return self.reply_text("您还没有加入任何会议")

            ans = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:15]+"..."
                else:
                    name = re['data'][index]['name']
                url = AddHeader('exit.html?'+str(re['data'][index]['id'])+ '@' +str(temp[0].user_id))
                ans.append({
                    'Title': name,
                    'Url': url,
                    'PicUrl': 'http://60.205.137.139/adminweb/'+ re['data'][index]['image'],
                })
            return self.reply_news(ans)
        else:
            return self.reply_text("您还没进行过绑定")


class FakeSearchHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['search'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            return self.reply_text('请输入关键词查询' + '\n' + '格式为：查询 关键词' + '\n' + '例：查询 教育资源')
        else:
            return self.reply_text("您还没进行过绑定")

class SearchHandler(WeChatHandler):

    def check(self):
        temp = self.input['Content'][:3]
        if(temp=="查询 "):
            return True
        else:
            return False

    def handle(self):
        checkContent = self.input['Content'][3:]
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/searchConfList?userid=' + str(
                temp[0].user_id) + '&content='+ urllib.parse.quote(checkContent) + '&page=' + str(1) + '&page_size=' + str(3)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)



            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data'][index]['id'],
                        name = mesre['data'][index]['name'],
                        start_date = mesre['data'][index]['start_date'],
                        end_date = mesre['data'][index]['end_date'],
                        logo = mesre['data'][index]['logo'],
                        location = mesre['data'][index]['location'],
                        image = mesre['data'][index]['image'],
                        version = mesre['data'][index]['version'],
                        private = mesre['data'][index]['private'],
                        private_type = mesre['data'][index]['privateType'],
                        sequence = mesre['data'][index]['sequence'],
                        status = mesre['data'][index]['status'],
                        desc = mesre['data'][index]['detail']['desc'],
                        website = mesre['data'][index]['detail']['website'],
                        phone = mesre['data'][index]['detail']['phone'],
                        fax = mesre['data'][index]['detail']['fax'],
                        email = mesre['data'][index]['detail']['email'],
                        wei_bo = mesre['data'][index]['detail']['weibo'],
                        wei_xin = mesre['data'][index]['detail']['weixin'],
                        qq = mesre['data'][index]['detail']['qq'],
                        longtitude = mesre['data'][index]['detail']['longtitude'],
                        latitude = mesre['data'][index]['detail']['latitude'],
                        timezone = mesre['data'][index]['detail']['timeZone'],
                    )
                    createActivity.save()


            if len(re['data']) == 0:
                return self.reply_text("没有查找到相关会议")

            ans = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:15] + "..."
                else:
                    name = re['data'][index]['name']
                if (temp[0].my_conf.all().filter(conf_id=re['data'][index]['id'])):
                    url = 'http://m2.huiplus.com.cn/app/#/confinfo/'+str(re['data'][index]['id'])
                else:
                    url = AddHeader('message.html?'+str(re['data'][index]['id']) + '@' +str(temp[0].user_id))
                ans.append({
                    'Title': name,
                    'Url': url,
                    'PicUrl': 'http://60.205.137.139/adminweb/' + re['data'][index]['image'],
                })
            return self.reply_news(ans)
        else:
            return self.reply_text("您还没进行过绑定")

class MeetingMessageHandler(WeChatHandler):
    def check(self):
        return self.is_event_click(self.view.event_keys['search'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            return self.reply_text('请输入关键词查询' + '\n' + '格式为：查询 关键词' + '\n' + '例：查询 教育资源')
        else:
            return self.reply_text("您还没进行过绑定")


class Quicklook(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['quick_look'])

    def handle(self):
        openid = self.input['FromUserName']
        temp = UserLogin.objects.filter(open_id=openid)
        if temp:
            url = 'http://60.205.137.139/adminweb/REST/API-V2/favoriteConfList?userid='+str(temp[0].user_id)+'&page='+str(1)+'&page_size='+str(3)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            content = response.read().decode('utf-8')
            re = json.loads(content)

            #用会议详情接口存信息
            for index in range(0, len(re['data'])):
                messageurl = 'http://60.205.137.139/adminweb/REST/API-V2/confInfo?confid=' + str(re['data'][index]['id'])
                messagereq = urllib.request.Request(messageurl)
                messageresponse = urllib.request.urlopen(messagereq)
                messagecontent = messageresponse.read().decode('utf-8')
                mesre = json.loads(messagecontent)
                if(not(ConfBasic.objects.filter(conf_id=re['data'][index]['id']))):
                    createActivity = ConfBasic.objects.create(
                        conf_id = mesre['data'][index]['id'],
                        name = mesre['data'][index]['name'],
                        start_date = mesre['data'][index]['start_date'],
                        end_date = mesre['data'][index]['end_date'],
                        logo = mesre['data'][index]['logo'],
                        location = mesre['data'][index]['location'],
                        image = mesre['data'][index]['image'],
                        version = mesre['data'][index]['version'],
                        private = mesre['data'][index]['private'],
                        private_type = mesre['data'][index]['privateType'],
                        sequence = mesre['data'][index]['sequence'],
                        status = mesre['data'][index]['status'],
                        desc = mesre['data'][index]['detail']['desc'],
                        website = mesre['data'][index]['detail']['website'],
                        phone = mesre['data'][index]['detail']['phone'],
                        fax = mesre['data'][index]['detail']['fax'],
                        email = mesre['data'][index]['detail']['email'],
                        wei_bo = mesre['data'][index]['detail']['weibo'],
                        wei_xin = mesre['data'][index]['detail']['weixin'],
                        qq = mesre['data'][index]['detail']['qq'],
                        longtitude = mesre['data'][index]['detail']['longtitude'],
                        latitude = mesre['data'][index]['detail']['latitude'],
                        timezone = mesre['data'][index]['detail']['timeZone'],
                    )
                    createActivity.save()




            if len(re['data']) == 0:
                return self.reply_text("您没有关注或收藏的会议")

            ans = "您的会议日程如下：\n"
            meetlist = []
            for index in range(0, len(re['data'])):
                if len(re['data'][index]['name']) > 15:
                    name = re['data'][index]['name'][:11]+"..."
                else:
                    name = re['data'][index]['name']
                starttime = re['data'][index]['start_date']
                meetlist.append((starttime,name))
                #ans.append({
                #    'Title': name,
                #    'Url': url,
                #    'PicUrl': 'http://60.205.137.139/adminweb/'+ re['data'][index]['image'],
                #})
            meetlist.sort()
            for i in meetlist:
                ans = ans + i[0] + "\n  " + i[1]
                if(i != meetlist[-1]):
                    ans = ans + "\n"
            return self.reply_text(ans)
        else:
            return self.reply_text("您还没进行过绑定")
