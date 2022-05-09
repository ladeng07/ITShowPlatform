from django.db import models


# Create your models here.
# class Department(models.Model):
#     class Meta:
#         verbose_name_plural = u"部门信息"
#
#     # department = [
#     #     (0, "系统维护"),
#     #     (1, "APP开发"),
#     #     (2, "Web开发"),
#     #     (3, "程序开发"),
#     #     (4, "游戏开发"),
#     #     (5, "UI设计")
#     # ]
#     # id = models.IntegerField(verbose_name="部门ID", choices=department, primary_key=True)
#     name = models.CharField(max_length=10, verbose_name="部门名称")
#     picture = models.ImageField(verbose_name="部门图标")
#
#     def __str__(self):
#         return self.name


class NewMember(models.Model):
    class Meta:
        verbose_name_plural = u"报名信息"

    schedules = [
        (1, "已报名"),
        (2, "初审中"),
        (3, "面试中"),
        (4, "笔试中"),
        (5, "成功录取"),
        (6, "初审失败"),
        (7, "面试失败"),
        (8, "笔试失败"),
        (9, "复试失败"),
        (10, "未录取")
    ]
    departments = [
        (0, "系统维护"),
        (1, "APP开发"),
        (2, "Web开发"),
        (3, "程序开发"),
        (4, "游戏开发"),
        (5, "UI设计")
    ]
    sex = [
        (0, "男"),
        (1, "女"),
        (2, "保密")
    ]
    name = models.CharField(max_length=20, verbose_name="姓名")
    sex = models.SmallIntegerField(choices=sex, default=2, verbose_name="性别")
    major = models.CharField(max_length=20, verbose_name="年级专业")
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="手机号码")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    department = models.SmallIntegerField(choices=departments, default=0,
                                          verbose_name="意向部门")
    expectation = models.TextField(max_length=200, verbose_name="期待的话")
    status = models.SmallIntegerField(choices=schedules, default=0, verbose_name="报名状态")

    def __str__(self):
        return self.name


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=5, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    # send_type = models.CharField(verbose_name="验证码类型", max_length=10,
    #                              choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)
