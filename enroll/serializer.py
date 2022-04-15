from rest_framework import serializers
from enroll.models import Department, New_member


class Department_serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class New_member_serializer(serializers.ModelSerializer):
    # verification_code = serializers.CharField(source="verification_code.code")

    class Meta:
        model = New_member
        exclude = ["id", "schedule"]

        extra_kwargs = {
            "name": {
                "error_messages": {
                    "max_length": "姓名过长"
                }
            },
            "phone_number": {
                "error_messages": {
                    "max_length": "手机号码不合规"
                }
            },
            "major": {
                "error_messages": {
                    "max_length": "文字过长"
                }
            }
        }
