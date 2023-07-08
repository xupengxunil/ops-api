from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register('group',views.ProjectGroupViewset,basename="group")
router.register('project',views.ProjectViewset,basename="project")
router.register('company',views.ProjectCompanyViewset,basename="company")
router.register('role',views.ProjectRoleViewset,basename="role")
router.register('user',views.ProjectUserViewSet,basename="user")

urlpatterns = [
    path("project/",include(router.urls))
]
