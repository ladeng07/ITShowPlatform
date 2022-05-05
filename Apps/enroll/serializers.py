from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from Apps.enroll.models import Department, NewMember, EmailVerifyRecord
import time
from utils.get_error_msg import get_error_msg


class department_serializer(serializers.ModelSerializer):
    """获取部门信息"""

    class Meta:
        model = Department
        fields = "__all__"


class new_member_serializer(serializers.ModelSerializer):
    """用于添加新成员时的校验与序列化"""

    # verification_code = serializers.CharField(source="verification_code.code")
    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=NewMember.objects.all(),
            message=get_error_msg(43032)
        )
    ])
    phone_number = serializers.CharField(validators=[
        UniqueValidator(
            queryset=NewMember.objects.all(),
            message=get_error_msg(43033)
        ),
    ],
        max_length=11, error_messages={"max_length": get_error_msg(42033)}
    )

    class Meta:
        model = NewMember
        exclude = ["id", "schedule"]

        extra_kwargs = {
            "name": {
                "error_messages": {
                    "max_length": get_error_msg(42034)
                }
            },
            "major": {
                "error_messages": {
                    "max_length": get_error_msg(42035)
                }
            },

        }


class new_member_schedule_serializer(serializers.ModelSerializer):
    """获取成员录取状态信息的序列化器"""

    class Meta:
        model = NewMember
        fields = ["name", "email", "schedule"]


class send_email_serializer(serializers.Serializer):
    """发送邮件时校验用序列化器"""

    # code = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=50,
                                   validators=[UniqueValidator(
                                       queryset=NewMember.objects.all(),
                                       message=get_error_msg(43032))],
                                   error_messages={"max_length": get_error_msg(42032), "invalid": get_error_msg(44036)})

    def validate_email(self, data):

        try:
            oj = EmailVerifyRecord.objects.get(email=data)
            # print(oj.email)/
            send_time = str(oj.send_time).split('+')[0].split('.')[0]
            send_time = time.mktime(time.strptime(send_time, '%Y-%m-%d %X'))
            now = time.time()
            # print(f"now={now},send={send_time}")
            if now - send_time < 120:
                raise serializers.ValidationError(code="verification_code", detail=get_error_msg(44033))
            else:
                # print(oj.email)
                oj.delete()
        except EmailVerifyRecord.DoesNotExist:
            pass