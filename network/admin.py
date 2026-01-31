# network/admin.py

from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html
from .models import NetworkNode, Contact, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset: QuerySet[NetworkNode]) -> None:
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "supplier_link", "debt", "created_at")
    list_filter = ("contact__city",)
    actions = (clear_debt,)

    def supplier_link(self, obj: NetworkNode) -> str:
        if not obj.supplier:
            return "-"
        url = reverse("admin:network_networknode_change", args=[obj.supplier.id])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

    supplier_link.short_description = "Поставщик"


# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)