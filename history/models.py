from django.db import models
from django.core.validators import validate_comma_separated_integer_list


class Department(models.Model):
    did = models.IntegerField("部门ID")
    department = models.CharField("部门", max_length=10)  # 如“程序部”
    department_en = models.CharField("部门英文名称", max_length=30)  # 如“程序部”
    part = models.IntegerField("部分", default=0)  # 0：内容一；1：内容二          （可能没必要）
    title = models.CharField("标题", max_length=30)  # 如部门介绍/部门要求
    content = models.CharField("内容", max_length=1500)  # 如部门介绍/部门要求

    class Meta:
        db_table = 'it_Department'
        verbose_name_plural = u'部门详情'

    
class History(models.Model):
    grade = models.IntegerField("年级")
    did = models.IntegerField("部门ID")
    department = models.CharField("部门", max_length=10)  # 如“程序部”

    class Meta:
        db_table = 'it_History'
        verbose_name_plural = u'历史表'


class Members(models.Model):
    # 默认id作为成员id
    id = models.IntegerField(primary_key=True)
    avatar = models.ImageField("头像", upload_to="avatar", blank=True)
    did = models.IntegerField("所属部门ID", default=0)
    grade = models.IntegerField("年级")
    name = models.CharField("成员姓名", max_length=10)
    motto = models.CharField("座右铭", max_length=30)
    department = models.CharField("所属部门", max_length=10)

    class Meta:
        db_table = 'it_Members'
        verbose_name_plural = u'部门成员'

