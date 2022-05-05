from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from Apps.enroll.models import Department, EmailVerifyRecord, NewMember
from Apps.enroll.serializers import department_serializer, new_member_serializer, new_member_schedule_serializer, \
    send_email_serializer
from rest_framework import status
from rest_framework.views import APIView
from Apps.enroll.email import send_code_email
from utils.get_error_msg import get_error_msg
import re
import time


class department_message(GenericAPIView):
    """获取部门信息"""

    queryset = Department.objects.all()
    serializer_class = department_serializer

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        # print(request.query_params)
        if request.query_params:
            return Response({"code": 40000, "msg": get_error_msg("40000")})
        return Response({"code": 20000, "msg": get_error_msg("20000"), "data": serializer.data})


class sign_up(GenericAPIView):
    """
    新成员报名
    post:提交新学员信息
    get:根据邮箱及手机号获取成员录取状态
    """

    serializer_class = new_member_serializer
    queryset = NewMember.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        code = data['verification_code']
        # print(f"code={code}")
        try:
            oj = EmailVerifyRecord.objects.get(email=data['email'])
            send_time = str(oj.send_time).split('+')[0].split('.')[0]
            send_time = time.mktime(time.strptime(send_time, '%Y-%m-%d %X'))
            now = time.time()
            if now - send_time > 120:
                return Response(
                    {"code": 40000, "msg": {"verification_code": get_error_msg(45032)}},
                    status=status.HTTP_400_BAD_REQUEST)
            if code != oj.code:
                return Response({"code": 45032, "msg": {"verification_code": get_error_msg(44031)}},
                                status=status.HTTP_400_BAD_REQUEST)
        except EmailVerifyRecord.DoesNotExist:
            return Response({"code": 44032, "msg": {"verification_code": get_error_msg(44032)}},
                            status=status.HTTP_400_BAD_REQUEST)
        ret = serializer.is_valid(raise_exception=False)
        if ret:
            serializer.save()
            return Response({"code": 20000, "msg": get_error_msg(20000)})
        else:
            error = {}
            for (i, j) in zip(serializer.errors.keys(), serializer.errors.values()):
                error[str(i)] = str(j[0])
            return Response({"code": 40000, "msg": error}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        string = request.query_params.get('string', '')
        try:
            if re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', string):
                queryset = self.get_queryset().get(email=string)
            elif re.match('^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$', string):
                queryset = self.get_queryset().get(phone_number=string)
            else:
                queryset = self.get_queryset().get(id=-1)
        except NewMember.DoesNotExist:
            return Response({"code": 40000, "msg": get_error_msg(45030)})
        serializer = new_member_schedule_serializer(instance=queryset)

        return Response({"code": 20000, "msg": get_error_msg(20000), "data": serializer.data})


class send_email(APIView):
    """发送邮件"""

    def post(self, request):
        data = request.data
        serializer = send_email_serializer(data=data)
        # code_serializer = Code_email_serializer()
        ret = serializer.is_valid()
        if ret:
            # serializer.save()
            send_code_email(data.get("email"))
            return Response({"code": 20000, "msg": get_error_msg(20000)})
        else:
            error = {}
            for (i, j) in zip(serializer.errors.keys(), serializer.errors.values()):
                error[str(i)] = str(j[0])
            return Response({"code": 40000, "msg": error}, status=status.HTTP_400_BAD_REQUEST)
