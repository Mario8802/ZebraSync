from django.contrib import admin
from .models import SyncJob, LogLine


@admin.register(SyncJob)
class SyncJobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("user__email",)


@admin.register(LogLine)
class LogLineAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "level", "message", "ts")
    list_filter = ("level", "ts")
    search_fields = ("message",)
