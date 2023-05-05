from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display =[
        "first_name",
        "last_name",
        "phone",
        "email",
    ]
    list_editable = [
        "phone",
        "email",
    ]
    search_fields = ['first_name__startswith', 'last_name__startswith']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=[
        "product",
        "get_customer_first_name",
        "get_customer_last_name",
        "quantity",
        "price",
        "address",
        "phone",
        "date",
        "status"
    ]

    list_editable = [
        "quantity",
        "price",
        "address",
        "phone",
        "status",
    ]

    search_fields = ['product']

    def get_customer_first_name(self, obj):
        return obj.customer.first_name
    
    def get_customer_last_name(self, obj):
        return obj.customer.last_name
    
    get_customer_first_name.short_description = 'Customer First Name'
    get_customer_last_name.short_description = 'Customer Last Name'
