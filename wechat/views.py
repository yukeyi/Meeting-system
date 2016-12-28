from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Activity
from meeting.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        Quicklook, ExitMeetingHandler, BindAccountHandler,  AllMeetingsHandler, RecentMeetingHandler, MyMeetingHandler, FakeSearchHandler, SearchHandler
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    event_keys = {
        'book_what': 'SERVICE_BOOK_WHAT',
        'get_ticket': 'SERVICE_GET_TICKET',
        'account_bind': 'SERVICE_BIND',
        'my_meeting': 'MY_MEETING',
        'exit_meeting': 'EXIT_MEETING',
        'quick_look': 'QUICK_LOOK',
        'book_empty': 'BOOKING_EMPTY',
        'book_header': 'BOOKING_ACTIVITY_',
        'all_meeting' : 'ALL_MEETING',
        'recent' : 'RECENT_MEETING',
        'search' : 'SEARCH_MEETING'
    }

    menu = {
        'button': [
            {
                "name": "我的会议",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "会佳账户绑定",
                        "key": event_keys['account_bind'],
                    },
                    {
                        "type": "click",
                        "name": "我收藏的会议",
                        "key": event_keys['my_meeting'],
                    },
                    {
                        "type": "click",
                        "name": "退出会议",
                        "key": event_keys['exit_meeting'],
                    },
                    {
                        "type": "click",
                        "name": "我的提醒",
                        "key": event_keys['quick_look'],
                    }
                ]
            },
            {
                "name": "服务",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "所有会议",
                        "key": event_keys['all_meeting'],
                    },
                    {
                        "type": "click",
                        "name": "近期会议",
                        "key": event_keys['recent'],
                    },
                    {
                        "type": "click",
                        "name": "查询会议",
                        "key": event_keys['search']
                    }
                ]
            }
        ]
    }

    @classmethod
    def get_book_btn(cls):
        return cls.menu['button'][-1]

    @classmethod
    def update_book_button(cls, activities):
        print("dfdf")



    @classmethod
    def update_menu(cls, activities=None):
        if activities is not None:
            if len(activities) > 5:
                cls.logger.warn('Custom menu with %d activities, keep only 5', len(activities))
            cls.update_book_button([{'id': act.id, 'name': act.name} for act in activities[:5]])
        else:
            current_menu = cls.lib.get_wechat_menu()
            existed_buttons = list()
            for btn in current_menu:
                if btn['name'] == '抢票':
                    existed_buttons += btn.get('sub_button', list())
            activity_ids = list()
            for btn in existed_buttons:
                if 'key' in btn:
                    activity_id = btn['key']
                    if activity_id.startswith(cls.event_keys['book_header']):
                        activity_id = activity_id[len(cls.event_keys['book_header']):]
                    if activity_id and activity_id.isdigit():
                        activity_ids.append(int(activity_id))
            return cls.update_menu(Activity.objects.filter(
                id__in=activity_ids, status=Activity.STATUS_PUBLISHED, book_end__gt=timezone.now()
            ).order_by('book_end')[: 5])
        cls.lib.set_wechat_menu(cls.menu)

