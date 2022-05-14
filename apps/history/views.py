from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.util import get_msg

from apps.history.models import Members, History, Department
from apps.history.serializers import MembersSerializer, HistorySerializer, DepartmentSerializer
import configparser,os
from ITShowPlatform.settings import BASE_DIR,MEDIA_URL

conf = configparser.RawConfigParser()

conf.read(os.path.join(BASE_DIR, "config.ini"), encoding="utf-8")

# class DepartmentViewSet(APIView):
#     # 获取部门信息
#     @method_decorator(csrf_exempt)
#     def get(self, request):
#         response = {
#             "code": 20000,
#             "msg": "成功",
#         }
#         obj = Department.objects.all().filter(did=request.GET.get('did')).first()  # 获取符合did的DepartmentObject
#         # （默认每个部门只对应一个object）
#         d = {'did': obj.did, 'department_cn': obj.department_cn, 'department_en': obj.department_en, 'content': obj.content,
#              'introduction': obj.introduction}  # 将其转为字典类（用于放入serializer检验）
#         serializer = DepartmentSerializer(data=d)
#         if serializer.is_valid():
#             response['data'] = serializer.data  # 在data里返回想得到的信息
#             return Response(data=response)
#         key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
#         # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
#         value = str(list(serializer.errors.get(key))[0]).split("-")
#         response['code'] = int(value[0])
#         response['msg'] = value[1]
#         return Response(data=response)

class DepartmentMessageView(GenericAPIView):
    """获取部门信息"""

    def get(self, request):
        queryset = Department.objects.all()

        if request.query_params:
            try:
                serializer = DepartmentSerializer(instance=queryset.get(id=request.query_params['id']))
                department_data = dict(serializer.data)
                department_data["background"] = conf.get("Django", "Host") + department_data["background"]
                department_data["icon"] = conf.get("Django", "Host") + department_data["icon"]
                return Response({"code": 20000, "msg": get_msg("20000"), "data": department_data})
            except Department.DoesNotExist:
                return Response({"code": 40000, "msg": "查询部门不存在"})
            # except TypeError:
            #     return Response({"code": 40000, "msg": "查询部门不存在"})
        else:
            serializer = DepartmentSerializer(instance=queryset, many=True)
            department_data = dict(serializer.data)
            department_data["background"] = conf.get("Django", "Host") + department_data["background"]
            department_data["icon"] = conf.get("Django", "Host") + department_data["icon"]
            return Response({"code": 20000, "msg": get_msg("20000"), "data": department_data})
        # print(request.query_params)


class MemberViewSet(APIView):
    # 获取历史成员信息
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        years = request.GET.get('years')
        department_id = request.GET.get('department_id')
        try:
            queryset = Members.objects.all().filter(Q(department_id=department_id) & Q(years=years))  # 获得所有符合要求的object
        except Members.DoesNotExist:
            response["code"] = 40000
            response["msg"] = "查询部门不存在"
            return Response(data=response)

        serializer = MembersSerializer(instance=queryset, many=True)
        for i in serializer.data:
            i["avatar"] = (conf.get("Django","Host") + i["avatar"])
        return Response({"code": 20000, "msg": get_msg("20000"), "data": serializer.data})
        # l = []  # 建一个列表用于存储最终输出的data
        # 对符合要求的每一个object都转为字典并通过serializer检验数据是否合法
        # for x in queryset:
        #     # avatar = str(x.avatar)
        #     # if avatar == '':
        #     #     avatar = "default/user.jpg"
        #     # 将符合要求的一个object都转为字典
        #     # d = {'id': x.id, 'department_id': x.department_id, 'grade': x.grade, 'department_cn': x.department_cn, 'motto': x.motto,
        #     #      'name': x.name,
        #     #      'avatar': avatar}  # 将路径转为字符串格式
        #     serializer = MembersSerializer(data=x)
        #     #if serializer.is_valid():
        #         l.append(d)  # 将合法数据存入l列表中并继续进行下一个循环
        #         continue
        # 若出现不合法数据则将错误信息返回前端
        #     key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
        #     # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
        #     value = str(list(serializer.errors.get(key))[0]).split("-")
        #     response['code'] = int(value[0])
        #     response['msg'] = value[1]
        #     return Response(data=response)
        # response['data'] = l
        # return Response(data=response)


class HistoryViewSet(APIView):
    # 获取历史列表
    @method_decorator(csrf_exempt)
    def get(self, request):
        response = {
            "code": 20000,
            "msg": "成功",
        }
        ser = History.objects.all().order_by("years")  # 获取全部历史列表信息
        # # 同上，对每一个object进行判断
        # for x in ser:
        #     d = {'department_id': x.department_id, 'grade': x.grade, 'department_cn': x.department_cn}
        #     serializer = HistorySerializer(data=d)
        #     if serializer.is_valid():
        #         continue
        #     key = list(serializer.errors.keys())[0]  # 得到错误信息的keys中的第一个key
        #     # 用一个key得到一个错误信息,一个错误信息中的错误码与detail用“-”隔开， 通过split分开
        #     value = str(list(serializer.errors.get(key))[0]).split("-")
        #     response['code'] = int(value[0])
        #     response['msg'] = value[1]
        #     return Response(data=response)
        # # 若数据通过判断，则在此处将数据转为要求格式
        data = []
        msg = {}
        if not ser:
            response["code"] = 40000
            response["msg"] = "查询部门不存在"
            return Response(data=response)
        for i in range(ser.first().years, ser.last().years + 1):
            msg["years"] = i
            msg["data"] = HistorySerializer(instance=ser.filter(years=i), many=True).data
            data.append(msg.copy())
            msg.clear()
            # data[i] = HistorySerializer(instance=ser.filter(years=i), many=True).data
        #     y = []
        #
        #     for j in range(0, Department.objects.count()):
        #         try:
        #             a = History.objects.get(Q(department_id=j) & Q(years=i))
        #         except History.DoesNotExist:  # 若为空，则继续判断下一个部门
        #             continue
        #
        #         x = {'id': a.department_id, 'department_name': a.department_cn}
        #         y.append(x)
        #     data['data'] = y
        #     info.append(data)
        response["data"] = data
        return Response(response)
