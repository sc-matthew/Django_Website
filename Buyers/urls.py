from django.contrib import admin
from django.urls import path, re_path
from .middlewares.auth import auth_middleware
from .views import Index, store, Signup, Login, logout, Cart, CheckOut, OrderView, Account, ProductDetailsView,product_search,Profile

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('account', Account.as_view(), name="account"),
    path('my_profile', Profile.as_view(), name="profile"),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('product_details/<int:product_id>/', ProductDetailsView.as_view(), name='product_details'),
    path('search/store', store , name='store'),
    path('search/', product_search, name='product_search'),
    path('search/product_details/<int:product_id>/', ProductDetailsView.as_view(), name='product_details_search'),
    # path('like', like_product, name = "like_product")
]