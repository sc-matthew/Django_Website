from django.contrib import admin
from .models import  Customer, Order


# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    list_editable = ["price"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
