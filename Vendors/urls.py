from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from .views import Homepage

urlpatterns = [
    path("", Homepage.as_view(), name="homepage")
]
