from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register('settings',views.SettingView,basename="settings")

urlpatterns = [
    path("settings/",include(router.urls))
]