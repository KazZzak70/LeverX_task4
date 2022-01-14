from django.contrib import admin
from courses.models import (
    Course,
    CourseMember,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("name", )


@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "course", )
    list_display_links = ("user", )
