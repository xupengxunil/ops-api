from rest_framework import status
from rest_framework.views import APIView

from common.custommodelviewset import CustomModelViewSet, ReadOnlyAdminModelViewSet
from common.customresponse import CustomResponse
from common.pages import CustomPagination
from libs.ssh import SSH
from apps.projects.models import Project
from .models import Host, HostUser, Config
from .other_views import fetch_host_extend
from .pages import MyPage
from .serializers import HostSerializer, HostUserSerializer, ConfigSerializer
from rest_framework import filters
from libs.decorators import auth


class HostView(APIView):

    # ListModelMixin->list

    def get(self, request, *args, **kwargs):
        queryset = Host.objects.all()
        if request.query_params['project'] != '':
            queryset = queryset.filter(project=request.query_params['project'])
        if request.query_params['env'] != '':
            queryset = queryset.filter(env=request.query_params['env'])
        if request.query_params['app'] != '':
            queryset = queryset.filter(app=request.query_params['app'])

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = HostSerializer(paginated_queryset, many=True)
        return CustomResponse(data=paginator.get_paginated_response(serializer.data), code=200, msg="OK", status=status.HTTP_200_OK)

    @auth('super')
    def post(self, request, *args, **kwargs):
        serializer = HostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            host = Host.objects.filter(ip_address=request.data['ip_address']).first()
            host_ip = host.ip_address
            host_pkey = host.private_key
            host_username = host.get_username()
            ssh = SSH(host_ip, '22', host_username, host_pkey)
            form = fetch_host_extend(ssh)
            host.os_version = form['os_name']
            host.disk_space = form['disk']
            host.cpu_cores = form['cpu']
            host.memory_size = int(form['memory'])
            host.save()
        except Exception as e:
            print(e)
            return CustomResponse(data=serializer.data, code=201, msg="获取主机信息失败", status=status.HTTP_201_CREATED)
        return CustomResponse(data=serializer.data, code=201, msg="OK", status=status.HTTP_201_CREATED)

    # patch update
    @auth('super')
    def patch(self, request, *args, **kwargs):
        id = request.query_params['id']
        host = Host.objects.filter(id=id).first()
        # 遍历request.data中的数据进行修改
        for k, v in request.data.items():
            if k == 'project':
                project = Project.objects.filter(id=v).first()
                setattr(host, k, project)
                continue
            print(k, v)
            setattr(host, k, v)
        host.save()
        return CustomResponse(data=[], code=200, msg="OK", status=status.HTTP_200_OK)

    # delete
    @auth('super')
    def delete(self, request, *args, **kwargs):
        id = request.query_params['id']
        try:
            Host.objects.filter(id=id).first().delete()
        except Exception as e:
            print(e)
            return CustomResponse(data=[], code=500, msg="删除失败", status=status.HTTP_204_NO_CONTENT)
        return CustomResponse(data=[], code=204, msg="OK", status=status.HTTP_204_NO_CONTENT)



class HostUserViewset(ReadOnlyAdminModelViewSet):
    queryset = HostUser.objects.all()
    serializer_class = HostUserSerializer
    pagination_class = MyPage

    # ListModelMixin->list

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)


class ConfigViewset(CustomModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['key']
    # ListModelMixin->list

    auth('super')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.query_params['project'] != '':
            queryset = queryset.filter(project=request.query_params['project'])
        if request.query_params['env'] != '':
            queryset = queryset.filter(env=request.query_params['env'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)


#修改root密码

class resetRootPassView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_superuser:
            return CustomResponse(data='', code=403, msg="无权限", status=status.HTTP_201_CREATED)
        host = Host.objects.filter(id=request.data['host_id']).first()
        host_ip = host.ip_address
        host_pkey = host.private_key
        host_username = host.get_username()
        ssh = SSH(host_ip, '22', host_username, host_pkey)
        with ssh:
            code, out = ssh.exec_command_raw('echo "root:%s" | chpasswd' % request.data['password'])
            if code != 0:
                return CustomResponse(data='', code=201, msg="修改失败", status=status.HTTP_201_CREATED)
        # 将密码进行base64加密后存入数据库
        from libs.utils import crypto_str
        host.root_password = crypto_str(request.data['password'])
        host.save()

        return CustomResponse(data='', code=200, msg="OK", status=status.HTTP_200_OK)

#查看root密码
class getRootPassView(APIView):
    def get(self, request):
        #检查用户权限
        user = request.user
        if not user.is_superuser:
            return CustomResponse(data='', code=403, msg="无权限", status=status.HTTP_201_CREATED)
        host = Host.objects.filter(id=request.query_params['id']).first()
        if host.root_password == '':
            return CustomResponse(data='', code=201, msg="未设置root密码", status=status.HTTP_201_CREATED)
        from libs.utils import decrypto_str
        root_password = decrypto_str(host.root_password)
        return CustomResponse(data={'password':root_password}, code=200, msg="OK", status=status.HTTP_200_OK)