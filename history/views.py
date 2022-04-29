from django.http import JsonResponse
from rest_framework.views import APIView
from history.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache


class DepartmentViewSet(APIView):
    # 获取部门信息
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        queryset = Department.objects.all().filter(did=request.GET.get('did'))
        serializer = DepartmentSerializer(queryset, many=True)
        try:
            response["data"] = serializer.data
        except:
            response['code'] = 40000
            response['msg'] = serializer.error_messages
        if len(response['data']) == 0:
            response['code'] = 40000
            response['msg'] = "未返回数据"
        else:
            response['code'] = 20000
            response['msg'] = "成功"
        return Response(data=response)


class MemberViewSet(APIView):
    # 获取历史成员信息
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        grade = request.GET.get('grade')
        did = request.GET.get('did')
        try:
            queryset = Members.objects.all().filter(Q(did=did) & Q(grade=grade))
            serializer = MembersSerializer(queryset, many=True)
        except:
            response = {
                "code": 40000,
                "msg": "错误",
            }
            return Response(data=response)
        response["data"] = serializer.data
        return Response(data=response)


class HistoryViewSet(APIView):
    # 获取历史列表
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        info = []
        for i in range(2002, 2022):
            data = {'grade': i}
            y = []
            for j in range(0, 6):
                try:
                    a = History.objects.get(Q(did=j) & Q(grade=i))
                except:
                    continue
                x = {'id': a.did, 'department_name': a.department}
                y.append(x)
            data['data'] = y
            info.append(data)
        response["data"] = info
        return Response(data=response)
