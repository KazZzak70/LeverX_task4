from django.contrib import admin
from reports.models import (
    Mark,
    Report,
    Comment,
)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("value", )
    list_display_links = ("value", )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("mark", "solution", "id", )
    list_display_links = ("solution", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("report", "role", "id", )
    list_display_links = ("report", )
