from rest_framework import serializers
from .models import *
from utils.get_error_msg import get_error_msg


class CommentsInfo(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content', 'post_time']

    post_time = serializers.DateTimeField(label="发布时间", required=False)
    content = serializers.CharField(label="弹幕内容", max_length=50, required=True)


    def validate_content(self, value):
        ban = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', "_", "-"]
        for i in ban:
            if i in value:
                raise serializers.ValidationError(code='40002', detail={'msg': get_error_msg(40002),
                                                                                  "code": '40002'})

        if len(value) > 50:
            raise serializers.ValidationError(code='40003', detail=get_error_msg(40003))
        elif len(value) == 0:
            raise serializers.ValidationError(code='40004', detail=get_error_msg(40004))


        return value
