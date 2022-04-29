import re

from rest_framework import serializers
from history.models import *
from django.core.validators import int_list_validator


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ('did', 'department_en', 'department', 'part', 'title', 'content')

    def validate_department(self, value):
        reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
        if not reg.match(value):
            raise serializers.ValidationError("只能输入汉字")
        return value

    def validate_department_en(self, value):
        reg = re.compile(r'^[A-Za-z]*$')
        if not reg.match(value):
            raise serializers.ValidationError("只能输入英文")
        return value

    did = serializers.IntegerField(required=True, error_messages={"blank": '部门ID不能为空', "invalid": '类型错误'})
    department = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
                                       validators=[validate_department],
                                       error_messages={"max_length": '长度过长', "blank": '部门名称不能为空'})
    department_en = serializers.CharField(max_length=30, required=True, trim_whitespace=True,
                                          validators=[validate_department_en],
                                          error_messages={"max_length": '长度过长', "blank": '部门英文名称不能为空'})
    part = serializers.IntegerField(required=True, error_messages={"blank": '不能为空'})  # 区分同意部分不同段落
    title = serializers.CharField(required=False, trim_whitespace=True, max_length=30,
                                  error_messages={"max_length": '题目过长'})
    content = serializers.CharField(max_length=600, required=True, trim_whitespace=True,
                                    error_messages={"max_length": '内容过长', "blank": '内容不能为空'})

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.department = validated_data.get("department", instance.department)
        instance.department_en = validated_data.get("department_en", instance.department_en)
        instance.id = validated_data.get("id", instance.id)
        instance.title = validated_data.get("title", instance.title)
        instance.part = validated_data.get("part", instance.part)
        instance.save()
        return instance


class MembersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Members
        fields = ('id', 'did', 'department', 'grade', 'name', 'motto', 'avatar')

    def name_validate(self, value):
        reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
        if not reg.match(value):
            raise serializers.ValidationError("只能输入汉字或英文")
        return value

    def validate_avatar(self, value):
        s = str(value)
        return s

    id = serializers.IntegerField()
    did = serializers.IntegerField(required=True, error_messages={"blank": '部门ID不能为空', "invalid": '类型错误'})
    department = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
                                       error_messages={"max_length": '部门名称过长', "blank": '部门名称不能为空'})
    grade = serializers.IntegerField(required=True, min_value=2001, max_value=2022,
                                     error_messages={"max_value": '年级数过大', "blank": "年级数不能为空", "min_value": '年级数过小'})
    name = serializers.CharField(required=True, trim_whitespace=True, max_length=6,
                                 error_messages={"blank": '姓名不能为空', "max_length": '姓名过长'})
    motto = serializers.CharField(required=False, trim_whitespace=True, max_length=25, validators=[name_validate],
                                  error_messages={"max_length": '座右铭过长'})
    avatar = serializers.ImageField(validators=[name_validate])

    def update(self, instance, validated_data):
        instance.did = validated_data.get("did", instance.did)
        instance.department = validated_data.get("department", instance.department)
        instance.grade = validated_data.get("grade", instance.grade)
        instance.name = validated_data.get("name", instance.name)
        instance.motto = validated_data.get("motto", instance.motto)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = History
        fields = ('grade', 'did', 'department')

    def validate_department(self, value):
        reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
        if not reg.match(value):
            raise serializers.ValidationError("只能输入汉字")
        return value

    grade = serializers.IntegerField(required=True, min_value=2001, max_value=2022,
                                     error_messages={"max_value": '年级数过大', "blank": "年级数不能为空", "min_value": '年级数过小'})
    did = serializers.IntegerField(required=True, error_messages={"blank": '部门ID不能为空', "invalid": '类型错误'})
    department = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
                                       validators=[validate_department],
                                       error_messages={"max_length": '部门名称过长', "blank": '部门名称不能为空'})

    def update(self, instance, validated_data):
        instance.department = validated_data.get("department", instance.department)
        instance.grade = validated_data.get("grade", instance.grade)
        instance.did = validated_data.get("did", instance.did)
        instance.save()
        return instance
