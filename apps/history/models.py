from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


GRADE_CHOICES = (
    (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009),
    (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016),
    (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)
)


class Department(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='部门ID')
    # did = models.IntegerField("部门ID")
    department_cn = models.CharField("部门名称", max_length=10)  # 如“程序部”
    department_en = models.CharField("部门英文名称", max_length=30)  # 如“程序部”
    picture = models.ImageField(verbose_name="部门图标", default=0)
    content = models.CharField("内容", max_length=800)  # 如部门介绍/部门要求
    introduction = models.CharField("介绍", max_length=800)  # 如部门介绍/部门要求
    status = models.SmallIntegerField("部门状态", choices=[(0, "解散"), (1, "健在")], default=1)

    class Meta:
        db_table = 'it_Department'
        verbose_name_plural = '部门详情'

    def __str__(self):
        return self.department_cn


class History(models.Model):
    # grade = models.IntegerField("年级")
    years = models.IntegerField("年份", default=int(datetime.now().strftime('%Y')), validators=[
        MaxValueValidator(2300),
        MinValueValidator(2010)
    ])
    # did = models.IntegerField("部门ID")
    # did = models.ForeignKey(Department, on_delete=models.DO_NOTHING(), related_name="history", verbose_name="部门id")
    # department_cn = models.CharField("部门", max_length=10)  # 如“程序部”
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="history", verbose_name="部门")

    class Meta:
        db_table = 'it_History'
        verbose_name_plural = '历史表'

    def __str__(self):
        return self.department


class Members(models.Model):
    # 默认id作为成员id
    avatar = models.ImageField("头像", upload_to="avatar", blank=True)
    # did = models.IntegerField("所属部门ID", default=0)
    grade = models.IntegerField("年级", choices=GRADE_CHOICES)
    name = models.CharField("成员姓名", max_length=10)
    motto = models.CharField("座右铭", max_length=30)
    # department_cn = models.CharField("所属部门", max_length=10)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="member",
                                   verbose_name="所属部门")

    class Meta:
        db_table = 'it_Members'
        verbose_name_plural = '部门成员'
