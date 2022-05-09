import time
from django.conf import settings
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Works
from .serializers import WorksInfoSerializer
# Create your views here.


class work(APIView):

    def get(self, request):
        key = []
        data = {"data": key}
        for i in range(2012, 2022):
            temp = {}
            try:
                works_set = Works.objects.filter(grade=i)
                if works_set:
                    serializer = WorksInfoSerializer(works_set, many=True)
                    temp['grade'] = i
                    temp['data'] = serializer.data
                    data['data'].append(temp)
            except Exception:
                pass
        if len(data['data']) == 0:
            data['code'] = 40000
            data['msg'] = "error"
        else:
            data['code'] = 20000
            data['msg'] = 'success'
        return Response(data=data)

