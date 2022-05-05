from django.db import models

# Create your models here.


class Comments(models.Model):
    post_time = models.DateTimeField(verbose_name="发布时间")
    content = models.CharField(verbose_name="弹幕内容", max_length=50, blank=False)



