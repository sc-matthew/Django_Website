from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from .views import Homepage, Signup, Login, Account, Image, logout, vendor_store, ProductDetails, AddProduct, EditProduct, DeleteProduct, DeleteConfirm, EditCategory, AddCategory, VendorDetail, vender_product_search 

urlpatterns = [
    path("", Homepage.as_view(), name="vendor_homepage"),
    path("signup", Signup.as_view(), name="vendor_signup"),
    path("login", Login.as_view(), name="vendor_login"),
    path("account_details", Account.as_view(), name="vendor_account_details"),
    path("account_image", Image.as_view(), name="vendor_account_image"),
    path("logout", logout, name="vendor_logout"),
    path("search/", vender_product_search, name="search"),
    path("my_products",vendor_store.as_view(), name="vendor_products"),
    path("my_products/<int:product_id>",ProductDetails.as_view(), name="vd_product_detail"),
    path("add_products", AddProduct.as_view(), name='add_product'),
    path("edit_products/<int:product_id>", EditProduct.as_view(), name='edit_product'),
    path("delete_confirm/<int:product_id>", DeleteConfirm.as_view(), name='delete_confirm'),
    path("delete_products/<int:product_id>", DeleteProduct.as_view(), name='delete_product'),
    path("add_products/add_category", AddCategory.as_view(),name = "add_category"),
    path("add_products/edit_category", EditCategory.as_view(),name = "edit_category"),
    path("profile/<int:vendorid>", VendorDetail.as_view(), name="vendor_detail")
]
