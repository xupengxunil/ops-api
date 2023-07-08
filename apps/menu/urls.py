from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register('menu',views.MenuViewset,basename="menu")
router.register('my',views.MenuViewset,basename="menu")

urlpatterns = [
    path("menu/",include(router.urls)),
    path("menu/treelist",views.MenuTreelist.as_view())
]
