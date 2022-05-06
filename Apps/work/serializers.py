from rest_framework import serializers
from .models import *


class WorksInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = '__all__'
    grade = serializers.CharField(label="年级", required=True)
    name = serializers.CharField(label="事件名称", max_length=30, required=True)
    description = serializers.CharField(label="事件描述", max_length=200, required=True)
    img = serializers.ImageField(label="图片", required=False)


    def validate_grade(self, value):
        if not (2010 < value <= 2021):
            raise serializers.ValidationError("不合法输入")
        return value