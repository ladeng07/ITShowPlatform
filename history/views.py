from rest_framework.views import APIView
from history.serializers import *
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
        obj = Department.objects.all().filter(did=request.GET.get('did')).first()  # 获取符合did的DepartmentObject
        # （默认每个部门只对应一个object）
        d = {'did': obj.did, 'department': obj.department, 'department_en': obj.department_en, 'content': obj.content,
             'introduction': obj.introduction}  # 将其转为字典类（用于放入serializer检验）
        serializer = DepartmentSerializer(data=d)
        if serializer.is_valid():
            response['data'] = serializer.data  # 在data里返回想得到的信息
            return Response(data=response)
        key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
        # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
        value = str(list(serializer.errors.get(key))[0]).split("-")
        response['code'] = int(value[0])
        response['msg'] = value[1]
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
        queryset = Members.objects.all().filter(Q(did=did) & Q(grade=grade))  # 获得所有符合要求的object
        l = []  # 建一个列表用于存储最终输出的data
        # 对符合要求的每一个object都转为字典并通过serializer检验数据是否合法
        for x in queryset:
            # 将符合要求的一个object都转为字典
            d = {'id': x.id, 'did': x.did, 'grade': x.grade, 'department': x.department, 'motto': x.motto,
                 'name': x.name,
                 'avatar': str(x.avatar)}  # 将路径转为字符串格式
            serializer = MembersSerializer(data=d)
            if serializer.is_valid():
                l.append(d)  # 将合法数据存入l列表中并继续进行下一个循环
                continue
            # 若出现不合法数据则将错误信息返回前端
            key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
            # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
            value = str(list(serializer.errors.get(key))[0]).split("-")
            response['code'] = int(value[0])
            response['msg'] = value[1]
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
        ser = History.objects.all()  # 获取全部历史列表信息
        # 同上，对每一个object进行判断
        for x in ser:
            d = {'did': x.did, 'grade': x.grade, 'department': x.department}
            serializer = HistorySerializer(data=d)
            if serializer.is_valid():
                continue
            key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
            # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
            value = str(list(serializer.errors.get(key))[0]).split("-")
            response['code'] = int(value[0])
            response['msg'] = value[1]
            return Response(data=response)
        # 若数据通过判断，则在此处将数据转为要求格式
        info = []
        for i in range(2002, 2022):
            data = {'grade': i}
            y = []
            for j in range(0, 6):
                try:
                    a = History.objects.get(Q(did=j) & Q(grade=i))
                except History.DoesNotExist:  # 若为空，则继续判断下一个部门
                    continue
                x = {'id': a.did, 'department_name': a.department}
                y.append(x)
            data['data'] = y
            info.append(data)
        response["data"] = info
        return Response(data=response)
