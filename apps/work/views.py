import time
from django.conf import settings
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Works
from .serializers import WorksInfoSerializer
from utils.get_msg import get_msg
import logging


# Create your views here.


class Work(APIView):
    """获取社团历年的作品"""

    def get(self, request):
        key = []
        data = {"data": key}
        for i in range(2002, 2022):
            """temp用来存储每个年级的作品，方便区分年级"""
            temp = {}
            try:
                works_set = Works.objects.filter(grade=i)
                if works_set:
                    serializer = WorksInfoSerializer(works_set, many=True)
                    temp['grade'] = i
                    temp['data'] = serializer.data
                    data['data'].append(temp)
            except Exception:
                """如果没有查到数据"""
                pass
        if len(data['data']) == 0:
            """如果查找的数据为空"""
            data['code'] = 45005
            data['msg'] = get_msg(45005)
        else:
            data['code'] = 20000
            data['msg'] = get_msg(20000)
        return Response(data=data)
