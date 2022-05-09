from pathlib import Path
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from apps.enroll.models import EmailVerifyRecord  # 邮箱验证model
from django.conf import settings  # setting.py添加的的配置信息
import random
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# 生成随机字符串
def random_str(randomlength=8):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送电子邮件
def send_code_email(email):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :return: True/False
    """
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = "".join([str(random.randint(0, 9)) for i in range(4)])
    email_record.code = code
    email_record.email = email
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    email_title = "注册激活"
    # file = open("/email_body")
    file = open(os.path.join(BASE_DIR, "enroll", "email_body"))
    email_body = str(file.read).format(code)
    # 发送邮件
    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    if not send_status:
        return False

    return True
