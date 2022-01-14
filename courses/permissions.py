from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.models import (
    Course,
    CourseMember,
)
from lectures.models import (
    Lecture,
    Hometask,
    Solution,
)
from reports.models import Report


class IsProfessorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        course = obj
        if isinstance(obj, Lecture):
            course = obj.course
        elif isinstance(obj, Solution):
            course = obj.task.lecture.course
        elif isinstance(obj, Report):
            course = obj.solution.task.lecture.course
        queryset_pr = CourseMember.objects.filter(user=request.user.id, course=course.id, role="PR")
        queryset_st = CourseMember.objects.filter(user=request.user.id, course=course.id, role="ST")
        if queryset_pr or (request.method in SAFE_METHODS and queryset_st):
            return True
        return False


class IsCourseMember(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        course = obj
        if isinstance(obj, Lecture):
            course = obj.course
        elif isinstance(obj, Hometask):
            course = obj.lecture.course
        queryset_st = CourseMember.objects.filter(user=request.user.id, course=course.id, role="ST")
        if queryset_st and request.method == "POST":
            return True
        return False


class IsReportOwner(BasePermission):

    def has_permission(self, request, view):
        courses = Course.objects.filter(
            coursemember__user__id=request.user.id,
            coursemember__role="PR",
        )
        report = get_object_or_404(klass=Report, id=request.data.get("report"))
        report_queryset = Report.objects.filter(solution__task__lecture__course__in=courses)
        if request.user.is_authenticated and (
                (report.solution.student.id == request.user.id and request.data.get("role") == "ST") or
                (report_queryset)
        ):
            return True
        return False
