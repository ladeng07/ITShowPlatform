from rest_framework import serializers
from .models import *


class CommentsInfo(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['content', 'post_time']

    post_time = serializers.DateTimeField(label="发布时间", required=False)
    content = serializers.CharField(label="弹幕内容", max_length=50, required=True)

    def validate_content(self, value):
        ban = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', "_", "-"]
        for i in ban:
            if i in value:
                raise serializers.ValidationError('非法字符')

        if len(value) > 50:
            raise serializers.ValidationError("弹幕过长")
        elif len(value) == 0:
            raise serializers.ValidationError("输入不能为空")


        return value
