"""ops_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from apps.simplejwt.views import MyTokenObtainPairView


urlpatterns = [

    path('api/', include('apps.users.urls')),
    path('api/', include('apps.menu.urls')),
    path('api/', include('apps.projects.urls')),
    path('api/', include('apps.resource.urls')),
    path('api/', include('apps.data.urls')),
    path('api/', include('apps.tools.urls')),
    path('api/', include('apps.settings.urls')),
    # 认证令牌
    path('api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="ops_api")),
]
