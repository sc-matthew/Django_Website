from django.contrib import admin
from . import models

@admin.register(models.Vendors)
class VendorsAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=[
        "store_name",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "open_hour",
        "to_hour",
    ]

    list_editable=[
        "email",
        "phone",
        "open_hour",
        "to_hour",
    ]

    search_fields = ["store_name"]

    def first_name(self, obj):
        return obj.contact_person_first_name
    
    def last_name(self, obj):
        return obj.contact_person_last_name
    
    first_name.short_description = "First Name"
    last_name.short_description = "Last Name"

@admin.register(models.Category_v)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display=[
        "name"
    ]

    search_fields=['name']

@admin.register(models.Products_v)
class ProductsAdmin(admin.ModelAdmin):
    list_per_page=10
    list_display=[
        "name",
        "price",
        "category",
        "last_update",
        "status",

    ]

    list_editable =[
        "price",
        "category",
        "status"
    ]

    search_fields = ['name']
