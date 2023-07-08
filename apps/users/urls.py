from django.urls import path,include
from rest_framework.routers import DefaultRouter

from apps.users import views

router = DefaultRouter()
router.register('user',views.UserInfoViewSet,basename="user")
router.register('role',views.RoleViewset,basename="role")

urlpatterns = [
    path("user/",include(router.urls)),
    path('user/userlist/', views.UserListView.as_view())
]