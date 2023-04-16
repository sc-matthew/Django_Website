from django.contrib import admin
from .models import Vendors, Products_v, Category_v

# Register your models here.
class AdminProduct_v(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_editable = ["price"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


# Register your models here.

# Register your models here.
admin.site.register(Vendors)
admin.site.register(Products_v,AdminProduct_v)
admin.site.register(Category_v)
