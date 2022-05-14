from django.db.models.signals import pre_save,pre_delete,post_init,post_save,pre_init
from django.dispatch import receiver

from .models import Works


# 修改时,保存图片并删除旧图
# @receiver(post_init, sender=Works)
# def file_path(sender, instance, **kwargs):
#     instance._current_image = instance.image


@receiver(pre_save, sender=Works)
def delete_old_image(sender, instance, **kwargs):
    print(instance.img)
    instance.img.delete(save=True)
