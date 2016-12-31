from django.db import models

from codex.baseerror import LogicError


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    #student_id = models.CharField(max_length=32, unique=True, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1


class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, db_index=True, unique=True)
    activity = models.ForeignKey(Activity)
    status = models.IntegerField()

    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2


class UserLogin(models.Model):
    user_id = models.IntegerField()
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.CharField(max_length=64, null=True)
    watching_page = models.IntegerField(default=1)
    my_conf = models.ManyToManyField('ConfBasic')

class ConfBasic(models.Model):
    conf_id = models.IntegerField()                   # 会议id
    name = models.CharField(max_length=128)           # 会议名
    start_date = models.DateField(db_index=True)      # 开始时间
    end_date = models.DateField(db_index=True)        # 结束时间
    location = models.CharField(max_length=256)       # 会议地点
    image = models.CharField(max_length=256)          # 图像
    version = models.IntegerField()                   # 会议版本
    private_type = models.IntegerField()              # 私有类型 0：公开 1：私有 2：收费
    color = models.CharField(max_length=64)           # 会议主色调
    sequence = models.CharField(max_length=64)        # 会议显示顺序号
    status = models.IntegerField()                    # 会议状态，详情见下面的状态定义
    preview_code = models.CharField(max_length=128)   # 私有码
    zipcode = models.CharField(max_length=8)          # 邮编
    decs = models.TextField()                         # 会议描述
    poster = models.CharField(max_length=256)         # 海报
    org = models.CharField(max_length=128)            # 组织方
    website = models.CharField(max_length=256)        # 网站
    reg_url = models.CharField(max_length=256)        # 注册会议的url
    phone = models.CharField(max_length=16)           # 联系电话
    fax = models.CharField(max_length=16)             # 传真
    email = models.CharField(max_length=64)
    wei_bo = models.CharField(max_length=64)
    wei_xin = models.CharField(max_length=64)
    qq = models.CharField(max_length=64)
    longitude = models.CharField(max_length=64)
    latitude = models.CharField(max_length=64)
    timezone = models.CharField(max_length=64)
    price = models.IntegerField()

    STATUS_INIT = 0
    STATUS_PREP = 1
    STATUS_TEST = 2
    STATUS_PUBLISH = 3
    STATUS_RESERVE = 4
    STATUS_END = 9