from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView

from common.custommodelviewset import CustomAdminModelViewSet,CustomModelViewSet
from common.customresponse import CustomResponse
from libs.decorators import auth
from .models import UserProfile,Role
from .serializers import UserSerializer, RoleSerializer, UserListSerializer
from .pages import MyPage


class UserInfoViewSet(CustomAdminModelViewSet):

    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields=['username']
    pagination_class = MyPage

    def get_queryset(self):
        return UserProfile.objects.filter()

    # def list(self, request):
    #     books = UserProfile.objects.all()
    #     serializer = UserSerializer(books, many=True)
    #     return Response(serializer.data)

class UserListView(APIView):
    @auth('super')
    def get(self,request):
        user=UserProfile.objects.all()
        serializer=UserListSerializer(user,many=True)
        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)

class RoleViewset(CustomModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class=MyPage

    # UpdateModelMixin->update
    @auth('super')
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return CustomResponse(data=serializer.data, code=200, msg="OK", status=status.HTTP_200_OK)

