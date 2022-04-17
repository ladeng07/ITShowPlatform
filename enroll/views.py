from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from enroll.models import Department, EmailVerifyRecord, New_member
from enroll.serializer import Department_serializer, New_member_serializer, New_member_schedule_serializer, \
    Send_email_serializer
from rest_framework import status
from rest_framework.views import APIView
from enroll.email import send_code_email
import re


class Department_message(GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = Department_serializer

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        # print(request.query_params)
        if request.query_params:
            return Response({"code": 40000, "msg": "请求失败"})
        return Response({"code": 20000, "msg": "成功", "data": serializer.data}, status=status.HTTP_200_OK)


class Sign_up(GenericAPIView):
    serializer_class = New_member_serializer
    queryset = New_member.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        code = data['verification_code']
        print(f"code={code}")
        try:
            if code != EmailVerifyRecord.objects.get(email=data['email']).code:
                return Response({"code": 40000, "msg": {"verification_code": "邮箱验证码错误"}},
                                status=status.HTTP_400_BAD_REQUEST)
        except EmailVerifyRecord.DoesNotExist:
            return Response({"code": 40000, "msg": {"verification_code": "请先发送验证码"}},
                            status=status.HTTP_400_BAD_REQUEST)
        ret = serializer.is_valid(raise_exception=False)
        # serializer.save()
        # print(serializer.errors)
        # ErrorDetail
        if ret:
            serializer.save()
        else:
            error = {}
            for (i, j) in zip(serializer.errors.keys(), serializer.errors.values()):
                error[str(i)] = str(j[0])
            return Response({"code": 40000, "msg": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"code": 20000, "msg": "成功"})

    def get(self, request):
        string = request.query_params.get('string', '')
        try:
            if re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', string):
                queryset = self.get_queryset().get(email=string)
            elif re.match('^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', string):
                queryset = self.get_queryset().get(phone_number=string)
            else:
                queryset = self.get_queryset().get(id=-1)
        except New_member.DoesNotExist:
            return Response({"code": 40000, "msg": "信息不存在"})
        serializer = New_member_schedule_serializer(instance=queryset)

        return Response({"code": 20000, "msg": "查询成功", "data": serializer.data})


class Send_email(APIView):
    def post(self, request):
        data = request.data
        serializer = Send_email_serializer(data=data)
        ret = serializer.is_valid()
        if ret:
            serializer.save()
        else:
            error = {}
            for (i, j) in zip(serializer.errors.keys(), serializer.errors.values()):
                error[str(i)] = str(j[0])
            return Response({"code": 40000, "msg": error}, status=status.HTTP_400_BAD_REQUEST)
        send_code_email(data.get("email"))
        return Response({"code": 20000, "msg": "成功"})
