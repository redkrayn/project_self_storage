from django.contrib import admin

# Register your models here.
from .models import Order, Cell, Warehouse, Request


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("cell", "start_date", "end_date")


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ("cell_id", "warehouse")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "created_at")
