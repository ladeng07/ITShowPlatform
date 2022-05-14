import time
from django.conf import settings
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Works
from .serializers import WorksInfoSerializer
from utils.util import get_msg,get_path
import logging
from rest_framework.generics import GenericAPIView
import configparser,os
from ITShowPlatform.settings import BASE_DIR,MEDIA_URL
from . import signals

conf = configparser.RawConfigParser()

conf.read(os.path.join(BASE_DIR, "config.ini"), encoding="utf-8")

# Create your views here.


class Work(GenericAPIView):
    """获取社团历年的作品"""

    def get(self, request):
        key = []
        data = {"data": key}
        for i in range(2022,2001,-1):
            """temp用来存储每个年级的作品，方便区分年级"""
            temp = {}
            #try:
            works_set = Works.objects.filter(grade=i)
            if works_set:
                serializer = WorksInfoSerializer(works_set, many=True)
                temp['grade'] = i
                temp['data'] = serializer.data
                for i in temp['data']:
                    i["img"] = get_path() + i["img"]
                data['data'].append(temp)
            # except Exception:
            #    """如果没有查到数据"""
            #    pass
        if len(data['data']) == 0:
            """如果查找的数据为空"""
            data['code'] = 45005
            data['msg'] = get_msg(45005)
        else:
            data['code'] = 20000
            data['msg'] = get_msg(20000)
        return Response(data=data)
