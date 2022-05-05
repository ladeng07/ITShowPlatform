from rest_framework.views import APIView
from Apps.history import *
from rest_framework.response import Response
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class DepartmentViewSet(APIView):
    # 获取部门信息
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        obj = Department.objects.all().filter(did=request.GET.get('did')).first()
        d = {'did': obj.did, 'department': obj.department, 'department_en': obj.department_en, 'content': obj.content,
             'introduction': obj.introduction}
        serializer = DepartmentSerializer(data=d)
        if serializer.is_valid():
            response['data'] = serializer.data
            return Response(data=response)
        response['code'] = 40000
        response['msg'] = "错误"
        response['data'] = serializer.errors
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
        queryset = Members.objects.all().filter(Q(did=did) & Q(grade=grade))
        l = []
        for x in queryset:
            d = {'id': x.id, 'did': x.did, 'grade': x.grade, 'department': x.department, 'motto': x.motto,
                 'name': x.name,
                 'avatar': str(x.avatar)}
            serializer = MembersSerializer(data=d)
            if serializer.is_valid():
                l.append(d)
                continue
            response = {
                "code": 40000,
                "msg": serializer.errors,
            }
            return Response(data=response)
        response['data'] = l
        return Response(data=response)


class HistoryViewSet(APIView):
    # 获取历史列表
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        ser = History.objects.all()
        for x in ser:
            d = {'did': x.did, 'grade': x.grade, 'department': x.department}
            serializer = HistorySerializer(data=d)
            if serializer.is_valid():
                continue
            response = {
                "code": 40000,
                "msg": serializer.errors,
            }
            return Response(data=response)
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
