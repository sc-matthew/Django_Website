from django.contrib import admin
from django.urls import path, re_path
from .views import Homepage


# URLConf
urlpatterns = [
    path("", Homepage.as_view(), name="homepage")]