from django.contrib import admin
from lectures.models import (
    Lecture,
    Hometask,
    Solution,
)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course", )
    list_display_links = ("name", )


@admin.register(Hometask)
class HometaskAdmin(admin.ModelAdmin):
    list_display = ("name", "lecture", "start_datetime", "deadline_datetime", "id", )
    list_display_links = ("name", )


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("task", "student", "status", "id", )
    list_display_links = ("task", )
