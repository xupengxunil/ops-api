from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views, other_views
router = DefaultRouter()
router.register('hostuser',views.HostUserViewset,basename="hostuser")
router.register('config',views.ConfigViewset,basename="config")

urlpatterns = [
    path("resource/",include(router.urls)),
    path("resource/syncosinfo/", other_views.OsInfoView.as_view()),
    path("resource/host/", views.HostView.as_view()),
    path("resource/deployhost/", other_views.DeployHostView.as_view()),
    path("resource/resetrootpass/", views.resetRootPassView.as_view()),
    path("resource/getrootpass/", views.getRootPassView.as_view()),
]
