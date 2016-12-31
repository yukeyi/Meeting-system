# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^message/?$', Postmessage.as_view()),
    url(r'^home/?$', Posthome.as_view()),
    url(r'^money/?$', Postmoney.as_view()),
    url(r'^meetlist/?$', Meetlist.as_view()),
    url(r'^joinin/?$', postJoinConf.as_view()),
    url(r'^exit/?$', postExitConf.as_view())
]
