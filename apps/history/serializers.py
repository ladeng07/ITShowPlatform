import re,os
from rest_framework import serializers
from ITShowPlatform.settings import BASE_DIR
from apps.history import *
from apps.history.models import Department, Members, History




# def validate_department(value):
#     reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
#     if not reg.match(value):
#         raise serializers.ValidationError("42011-部门名称中只能输入汉字或英文")
#
#
# def validate_department_en(value):
#     reg = re.compile(r'^[A-Za-z][A-Za-z\s]*$')
#     if not reg.match(value):
#         raise serializers.ValidationError("42010-部门英文名称中只能输入英文")
#
#
# def name_validate(value):
#     reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
#     if not reg.match(value):
#         raise serializers.ValidationError("42012-姓名只能输入汉字或英文")


#
# def validate_avatar(value):
#     s = str(value)
#     return s


# class DepartmentSerializer(serializers.Serializer):
#     did = serializers.IntegerField(required=True, error_messages={"blank": '41010-部门ID不能为空', "invalid": '42020-类型错误'})
#     department_cn = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
#                                           validators=[validate_department],
#                                           error_messages={"max_length": '42021-部门名称长度过长', "blank": '41011-部门名称不能为空'})
#     department_en = serializers.CharField(max_length=30, required=True, trim_whitespace=True,
#                                           validators=[validate_department_en],
#                                           error_messages={"max_length": '42022-部门英文名称长度过长',
#                                                           "blank": '41012-部门英文名称不能为空'})
#     content = serializers.CharField(max_length=800, required=True, trim_whitespace=True,
#                                     error_messages={"max_length": '42023-内容过长', "blank": '41013-内容不能为空'})
#     introduction = serializers.CharField(max_length=800, required=True, trim_whitespace=True,
#                                          error_messages={"max_length": '42024-介绍内容过长', "blank": '41014-介绍内容不能为空'})
#
#     # class Meta:
#     #     model = Department
#     #     fields = ('did', 'department_en', 'department_cn', 'part', 'title', 'content')
#
#     def create(self, validated_data):
#         return Department.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.content = validated_data.get("content", instance.content)
#         instance.department_cn = validated_data.get("department_cn", instance.department_cn)
#         instance.department_en = validated_data.get("department_en", instance.department_en)
#         instance.id = validated_data.get("id", instance.id)
#         instance.title = validated_data.get("title", instance.title)
#         instance.part = validated_data.get("part", instance.part)
#         instance.save()
#         return instance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

        extra_kwargs = {
            "department_cn": {
                "error_messages": {
                    "max_length": '42021-部门名称长度过长',
                    "blank": '41011-部门名称不能为空'
                }
            },
            "department_en": {
                "error_messages": {
                    "max_length": '42022-部门英文名称长度过长',
                    "blank": '41012-部门英文名称不能为空'
                }
            },
            "content": {
                "error_messages": {
                    "max_length": '42023-内容过长',
                    "blank": '41013-内容不能为空'
                }
            },
            "introduction": {
                "error_messages": {
                    "max_length": '42024-介绍内容过长',
                    "blank": '41014-介绍内容不能为空'
                }
            }
        }

    def validate_department_cn(self, data):
        reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
        if not reg.match(data):
            raise serializers.ValidationError("42011-部门名称中只能输入汉字或英文")
        return data

    def validate_department_en(self, data):
        reg = re.compile(r'^[A-Za-z][A-Za-z\s]*$')
        if not reg.match(data):
            raise serializers.ValidationError("42010-部门英文名称中只能输入英文")
        return data

    def validate_name(self, data):
        reg = re.compile(r'^[\u4e00-\u9fa5A-Za-z]*$')
        if not reg.match(data):
            raise serializers.ValidationError("42012-姓名只能输入汉字或英文")
        return data

    def validate_id(self,data):
        obj = Department.objects.filter(id=data)
        if not obj:
            raise serializers.ValidationError("查询的部门不存在")
        return data


# class MembersSerializer(serializers.HyperlinkedModelSerializer):
#     did = serializers.IntegerField(required=True, error_messages={"blank": '41010-部门ID不能为空', "invalid": '42020-类型错误'})
#     department = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
#                                        error_messages={"max_length": '42021-部门名称过长', "blank": '41011-部门名称不能为空'})
#     grade = serializers.IntegerField(required=True, min_value=2001, max_value=2022,
#                                      error_messages={"max_value": '42025-年级数过大', "blank": "41015-年级数不能为空",
#                                                      "min_value": '42026-年级数过小'})
#     name = serializers.CharField(required=True, trim_whitespace=True, max_length=6,
#                                  error_messages={"blank": '41016-姓名不能为空', "max_length": '42027-姓名过长'})
#     motto = serializers.CharField(required=False, trim_whitespace=True, max_length=25, validators=[name_validate],
#                                   error_messages={"max_length": '42028-座右铭过长'})
#
#     # avatar = serializers.ImageField(validators=[validate_avatar])
#
#     class Meta:
#         model = Members
#         fields = ('did', 'department_cn', 'grade', 'name', 'motto')
#
#     def create(self, validated_data):
#         return Members.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.did = validated_data.get("did", instance.did)
#         instance.department_cn = validated_data.get("department_cn", instance.department_cn)
#         instance.grade = validated_data.get("grade", instance.grade)
#         instance.name = validated_data.get("name", instance.name)
#         instance.motto = validated_data.get("motto", instance.motto)
#         instance.avatar = validated_data.get("avatar", instance.avatar)
#         instance.save()
#         return instance

class MembersSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.department_cn")
    class Meta:
        model = Members
        fields = ("id",'department', 'years', 'name', 'motto','avatar')

        extra_kwargs = {
            "department": {
                "error_messages": {
                    "max_length": '42021-部门名称过长',
                    "blank": '41011-部门名称不能为空'
                }
            },
            "grade": {
                "error_messages": {
                    "max_value": '42025-年级数过大',
                    "blank": "41015-年级数不能为空",
                    "min_value": '42026-年级数过小'
                }
            },
            "name": {
                "error_messages": {
                    "blank": '41016-姓名不能为空',
                    "max_length": '42027-姓名过长'
                }
            },
            "motto": {
                "error_messages": {
                    "max_length": '42028-座右铭过长'
                }
            }

        }





# class HistorySerializer(serializers.Serializer):
#     grade = serializers.IntegerField(required=True, min_value=2001, max_value=2022,
#                                      error_messages={"max_value": '42025-年级数过大', "blank": "41015-年级数不能为空",
#                                                      "min_value": '42026-年级数过小'})
#     did = serializers.IntegerField(required=True, error_messages={"blank": '41010-部门ID不能为空', "invalid": '42020-类型错误'})
#     department = serializers.CharField(max_length=10, required=True, trim_whitespace=True,
#                                        validators=[validate_department],
#                                        error_messages={"max_length": '42021-部门名称过长', "blank": '41011-部门名称不能为空'})
#
#     # class Meta:
#     #     model = History
#     #     fields = ('grade', 'did', 'department_cn')
#     #
#
#     def create(self, validated_data):
#         return History.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.department_cn = validated_data.get("department_cn", instance.department_cn)
#         instance.grade = validated_data.get("grade", instance.grade)
#         instance.did = validated_data.get("did", instance.did)
#         instance.save()
#         return instance

class HistorySerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.department_cn")
    id = serializers.IntegerField(source="department.id")
    class Meta:
        model = History
        fields = ('id', 'department')
