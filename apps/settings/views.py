from rest_framework import filters
from rest_framework import status

from common.custommodelviewset import CustomAdminModelViewSet
from common.customresponse import CustomResponse
from .models import Setting
from .serializers import SettingsSerializer
from common.pages import MyPage
import json
from libs.decorators import auth


class SettingView(CustomAdminModelViewSet):

    queryset = Setting.objects.all()
    serializer_class = SettingsSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['key']

    @auth('super')
    def create(self, request, *args, **kwargs):
        set = Setting()
        set.key = request.data.get('key')
        set.value = json.dumps(request.data.get('value'))
        set.desc = request.data.get('desc')
        set.save()
        return CustomResponse(data={}, code=201, msg="新增成功", status=status.HTTP_201_CREATED)

    @auth('super')
    def update(self, request, *args, **kwargs):
        set = Setting.objects.get(key=request.data.get('key'))
        set.value = json.dumps(request.data.get('value'))
        set.desc = request.data.get('desc')
        set.save()
        return CustomResponse(data={}, code=201, msg="更新成功", status=status.HTTP_200_OK)