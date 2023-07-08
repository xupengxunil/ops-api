from .views import *
from django.urls import path

urlpatterns = [
    path('data/statics/', DataView.as_view()),
]