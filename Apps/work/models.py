from django.db import models

# Create your models here.


class Works(models.Model):
    grade = models.IntegerField(verbose_name="年份")
    name = models.CharField(verbose_name="事件名称", max_length=30)
    description = models.CharField(verbose_name="事件描述", max_length=200)
    img = models.ImageField(verbose_name="图片", upload_to="image", null=True, blank=True)
