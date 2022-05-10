import time, datetime
from django.conf import settings
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import CommentsInfo
from django.utils import timezone
from utils.get_msg import get_msg
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class CommentView(APIView):
    """获取弹幕的内容"""
    def get(self, request):
        data = {}
        queryset = Comments.objects.all()
        serializer = CommentsInfo(queryset, many=True)
        try:
            data['data'] = serializer.data
        except:
            data['msg'] = serializer.error_messages
        if len(data['data']) == 0:
            """如果没有获取到数据"""
            data['msg'] = get_msg(40005)
            data['code'] = 40005
        else:
            data['msg'] = get_msg(20000)
            data['code'] = 20000
        return Response(data=data)

    """接收新弹幕"""
    @csrf_exempt
    def post(self, request):
        data = {}
        serializer = CommentsInfo(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            data['msg'] = get_msg(50000)
            data['code'] = 50000
            return Response(data=data)
        try:
            length = serializer.validated_data['content']
            data['msg'] = "success"
            data['code'] = 20000
        except KeyError:
            data['code'] = 42003
            data['msg'] = get_msg(42003)
            return Response(data=data)
        """时间不用保存到毫秒"""
        serializer.validated_data['post_time'] = timezone.now().replace(microsecond=0)
        serializer.save()
        data['data'] = serializer.validated_data

        return Response(data=data)

