import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from apps.settings.utils import AppSetting

from libs.ldap import LDAP

from common.customresponse import CustomResponse
from apps.users.models import UserProfile
from .serializers import MyTokenObtainPairSerializer


def auth_user(username, password):
    try:
        conf = AppSetting.get('ldap')
        config = json.loads(conf)
        ldap = LDAP(**config)
        is_success, message = ldap.valid_user(username, password)
        if is_success:
            return True
        elif message:
            return False
    except Exception as e:
        print(e)
        return False


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    # post方法对应post请求，登陆时post请求在这里处理
    def post(self, request, *args, **kwargs):
        # 使用刚刚编写时序列化处理登陆验证及数据响应
        print(request.data)
        if request.data['ldap'] == 1 and request.data['username'] != 'admin':
            ret = auth_user(request.data['username'], request.data['password'])
            if ret:
                try:
                    user = UserProfile.objects.get(username=request.data['username'])
                except ObjectDoesNotExist as e:
                    user = UserProfile()
                    user.name = request.data['username']
                    user.username = request.data['username']
                    user.role_id = 99
                    user.save()
                    data = {}
                    refresh = RefreshToken.for_user(user)
                    print('Token,{}'.format(str(refresh.access_token)))
                    data['refresh'] = str(refresh)
                    data['token'] = str(refresh.access_token)
                    data['id'] = user.id
                    data['username'] = user.username
                    return CustomResponse(data={'data':data}, code=200, msg="OK", status=status.HTTP_200_OK)
                finally:
                    if not user.is_active:
                        return CustomResponse(data='账户已冻结', code=401, msg="error", status=status.HTTP_401_UNAUTHORIZED)
                    data = {}
                    refresh = RefreshToken.for_user(user)
                    print('Token,{}'.format(str(refresh.access_token)))
                    data['refresh'] = str(refresh)
                    data['token'] = str(refresh.access_token)
                    data['id'] = user.id
                    data['username'] = user.username
                    return CustomResponse(data={'data':data}, code=200, msg="OK", status=status.HTTP_200_OK)
                # password error
            else:
                return CustomResponse(data={"Ldap not authed."}, code=401, msg="Failed",
                                      status=status.HTTP_401_UNAUTHORIZED)

        print(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise ValueError(f'验证失败： {e}')

        return CustomResponse(data=serializer.validated_data, code=200, msg="OK", status=status.HTTP_200_OK)
