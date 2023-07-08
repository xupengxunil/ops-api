import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from common.customresponse import CustomResponse
from apps.users.models import UserProfile, Role
from apps.users.serializers import UserSerializer
from .models import Menu
from .serializers import MenuSerializer

# Create your views here.
from common.custommodelviewset import CustomModelViewSet,ReadOnlyAdminModelViewSet


def to_new_res(res, list):
    for parent in res:
        tmp_children = []
        for menu in list:
            if int(menu['parentId']) == parent['id']:
                tmp_children.append(menu)
        if tmp_children:
            parent['children'] = tmp_children
    return res

def to_new_res_three(res, list):
    for parent in res:
        if 'children' in parent:
            for child in parent['children']:
                tmp_children = []
                for menu in list:
                    if int(menu['parentId']) == child['id']:
                        tmp_children.append(menu)
                if tmp_children:
                    child['children'] = tmp_children
    return res

def to_new_treelist(res, list):
    for parent in res:
        tmp_children = []
        for menu in list:
            if int(menu['parentId']) == parent['value']:
                node = {}
                node['value'] = menu['id']
                node['label'] = menu['name']
                tmp_children.append(node)
        if tmp_children:
            parent['children'] = tmp_children
    return res

def to_new_treelist_three(res, list):
    for parent in res:
        if 'children' in parent:
            for child in parent['children']:
                tmp_children = []
                for menu in list:
                    if int(menu['parentId']) == child['value']:
                        node = {}
                        node['value'] = menu['id']
                        node['label'] = menu['name']
                        tmp_children.append(node)
                if tmp_children:
                    child['children'] = tmp_children
    return res


class  MenuViewset(ReadOnlyAdminModelViewSet):
    '''
    首页轮播图的商品
    '''
    queryset = Menu.objects.all().order_by("sort")
    serializer_class = MenuSerializer

    # pagination_class = MyPage

    def list(self, request, *args, **kwargs):
        print(self.request.user)
        user = UserProfile.objects.filter(id=request.user.id).first()
        menuList = {}
        if (user.username == 'admin'):
            menuList = Menu.objects.all().order_by('sort')
        else:
            role = Role.objects.filter(id=user.role_id).first()
            if role.menulist == '':
                return CustomResponse(data={}, code=200, msg="OK", status=status.HTTP_200_OK)
            else:
                menuId = role.menulist.split(',')
                menuList = Menu.objects.filter(id__in=menuId).all().order_by('sort')

        menuList = MenuSerializer(menuList, many=True).data

        res = []
        for menu in menuList:
            if menu['type'] == 1:
                res.append(menu)

        res = to_new_res(res, menuList)
        res = to_new_res_three(res, menuList)

        return CustomResponse(data={"user": UserSerializer(user).data, "menu": res}, code=200, msg="OK",
                              status=status.HTTP_200_OK)


class MenuTreelist(APIView):


    def get(self, request, *args, **kwargs):
        print(self.request.user)
        user = UserProfile.objects.filter(id=request.user.id).first()
        menuList = {}
        if (user.role_id == 1):
            menuList = Menu.objects.all().order_by('sort')
        else:
            role = Role.objects.filter(id=user.role_id).first()
            if role.menulist == '':
                return CustomResponse(data={}, code=200, msg="OK", status=status.HTTP_200_OK)
            else:
                menuId = role.menulist.split(',')
                menuList = Menu.objects.filter(id__in=menuId).all().order_by('sort')

        menuList = MenuSerializer(menuList, many=True).data


        res = []
        for menu in menuList:
            if menu['type'] == 1:
                node = {}
                node['value'] = menu['id']
                node['label'] = menu['name']
                res.append(node)

        res = to_new_treelist(res, menuList)
        res = to_new_treelist_three(res, menuList)

        all_node = []
        root_node = {}
        root_node['value'] = 0
        root_node['label'] = '根目录'
        root_node['children'] = res

        all_node.append(root_node)

        return CustomResponse(data={'treelist':all_node}, code=200, msg="OK",
                              status=status.HTTP_200_OK)