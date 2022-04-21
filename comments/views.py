import time, datetime
from django.conf import settings
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import CommentsInfo
from django.utils import timezone
# Create your views here.


class comments(APIView):

    def get(self, request):
        data = {}
        queryset = Comments.objects.all()
        serializer = CommentsInfo(queryset, many=True)
        try:
            data['data'] = serializer.data
        except:
            data['msg'] = serializer.error_messages
        if len(data['data']) == 0:
            data['msg'] = 'error'
            data['code'] = "40000"
        else:
            data['msg'] = "success"
            data['code'] = "20000"
        return Response(data=data)


    def post(self, request):
        data = {}
        serializer = CommentsInfo(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            data['msg'] = serializer.error_messages
            data['code'] = "40000"
            return Response(data=data)
        serializer.validated_data['post_time'] = timezone.now().replace(microsecond=0)
        serializer.save()
        data['data'] = serializer.validated_data
        data['msg'] = "success"
        data['code'] = "20000"
        return Response(data=data)

