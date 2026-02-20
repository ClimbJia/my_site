from django.contrib import admin

from .models import DemoRequest, SchemeRequest, DownloadLead


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "kindergarten", "city", "created_at"]
    list_filter = ["city", "created_at"]
    search_fields = ["name", "phone", "kindergarten"]


@admin.register(SchemeRequest)
class SchemeRequestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "kindergarten",
        "city",
        "is_processed",
        "created_at",
    ]
    list_filter = ["city", "is_processed", "created_at"]
    search_fields = ["name", "phone", "kindergarten", "city"]


@admin.register(DownloadLead)
class DownloadLeadAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "kindergarten",
        "city",
        "product_name",
        "file_name",
        "created_at",
    ]
    list_filter = ["city", "product_name", "created_at"]
    search_fields = ["name", "phone", "kindergarten", "product_name", "file_name"]
