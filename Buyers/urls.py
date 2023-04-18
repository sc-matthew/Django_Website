from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from . import views
from .views import Index, store, Signup, Login, logout, Cart, CheckOut, OrderView,product_details, add_to_cart, like_product, product_search

# URLConf
urlpatterns = [
    path("", Index.as_view(), name="homepage"),
    path("store/", store, name="store"),
    path("signup", Signup.as_view(), name="signup"),
    path("login", Login.as_view(), name="login"),
    path("logout", logout, name="logout"),
    path("cart", auth_middleware(Cart.as_view()), name="cart"),
    path("check-out", CheckOut.as_view(), name="checkout"),
    path('store/product_details/<int:product_id>/', product_details.as_view(), name='product_details'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('product_details/<int:product_id>/like/', like_product, name='like_product'),
    path('search/', product_search, name='product_search')

]
