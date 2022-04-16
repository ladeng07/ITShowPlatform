from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from enroll.models import Department, New_member


class Department_serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class New_member_serializer(serializers.ModelSerializer):
    # verification_code = serializers.CharField(source="verification_code.code")
    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=New_member.objects.all(),
            message="该邮箱已存在"
        )
    ])
    phone_number = serializers.CharField(validators=[
        UniqueValidator(
            queryset=New_member.objects.all(),
            message="该手机号码已存在"
        ),
    ],
        max_length=11, error_messages={"max_length": "手机号码不合规"}
    )

    class Meta:
        model = New_member
        exclude = ["id", "schedule"]

        extra_kwargs = {
            "name": {
                "error_messages": {
                    "max_length": "姓名过长"
                }
            },
            "major": {
                "error_messages": {
                    "max_length": "文字过长"
                }
            },

        }

    def validate_code(self, data):
        print(f"email={self.email}")
        return data


class New_member_schedule_serializer(serializers.ModelSerializer):
    class Meta:
        model = New_member
        fields = ["name", "email", "schedule"]


class Send_email_serializer(serializers.Serializer):
    # code = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=50,
                                   validators=[UniqueValidator(
                                       queryset=New_member.objects.all(),
                                       message="该邮箱已存在")],
                                   error_messages={"max_length": "邮箱过长", "invalid": "请输入正确格式的邮箱"})
