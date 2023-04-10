from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from .views import Homepage, Signup, Login, Test

urlpatterns = [
    path("", Homepage.as_view(), name="vendor_homepage"),
    path("signup", Signup.as_view(), name="vendor_signup"),
    path("login", Login.as_view(), name="vendor_login"),
    path("test", Test.as_view(), name="vendor_test"),
]
