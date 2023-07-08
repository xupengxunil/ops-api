from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register('todolist',views.TodolistViewset,basename="todolist")

urlpatterns = [
    path("tools/",include(router.urls)),
]
