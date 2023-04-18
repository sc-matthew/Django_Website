from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from .views import Homepage, Signup, Login, Account, Image, logout, vendor_store, AddProductView

urlpatterns = [
    path("", Homepage.as_view(), name="vendor_homepage"),
    path("signup", Signup.as_view(), name="vendor_signup"),
    path("login", Login.as_view(), name="vendor_login"),
    path("account_details", Account.as_view(), name="vendor_account_details"),
    path("account_image", Image.as_view(), name="vendor_account_image"),
    path("logout", logout, name="vendor_logout"),
    path("my_products",vendor_store.as_view(), name="vendor_products"),
    path("add_products", AddProductView.as_view(), name='add_product'),
    path("edit_products", AddProductView.as_view(), name='edit_product')
]
