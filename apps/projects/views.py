from django.shortcuts import render
from rest_framework import mixins, viewsets

from common.custommodelviewset import ReadOnlyAdminModelViewSet
from rest_framework import filters

from common.customresponse import CustomResponse
from libs.decorators import auth
from .pages import MyPage
from rest_framework import status
from .models import Project, Role, Group, Company, ProjectUser
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from .serializers import ProjectSerializer, GroupSerializer, CompanySerializer, RoleSerializer, ProjectUserSerializer


class ProjectCompanyViewset(ReadOnlyAdminModelViewSet):
    '''
    子公司管理视图
    '''
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['company_nickname', 'company_code', 'company_name']

class ProjectGroupViewset(ReadOnlyAdminModelViewSet):
    '''
    项目GROUP管理视图
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['group_code', 'group_name']


class ProjectViewset(ReadOnlyAdminModelViewSet):
    '''
    项目管理视图
    '''
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['project_name', 'project_code']

    # ListModelMixin->list
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)

class ProjectRoleViewset(ReadOnlyAdminModelViewSet):
    '''
    项目角色管理视图
    '''
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['role_name', 'role_code']




class ProjectUserViewSet(ReadOnlyAdminModelViewSet):
    '''
    项目用户管理视图
    '''
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    pagination_class = MyPage
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['project', 'user']

    @auth('super')
    def list(self, request, *args, **kwargs):
        if 'project' in request.query_params:
            project_id = int(request.query_params['project'])
            projectUser = ProjectUser.objects.filter(project=project_id)
            serializer = self.get_serializer(projectUser, many=True)
        else:
            return CustomResponse(data={}, code=200, msg="No id request.", status=status.HTTP_200_OK)
        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)
