from django.contrib import admin

# Register your models here.
from .models import Order, Cell, Warehouse, Request
from django.db.models import Exists, OuterRef

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("cell", "start_date", "end_date", "adv_id")
    list_filter = ("adv_id",)
    search_fields = ("adv_id",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cell":
            kwargs["queryset"] = Cell.objects.annotate(
                has_order=Exists(
                    Order.objects.filter(
                        cell=OuterRef("pk"), is_active=True
                    )
                )
            ).filter(has_order=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ("cell_id", "warehouse")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "created_at")
