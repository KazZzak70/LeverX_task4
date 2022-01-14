from rest_framework import generics
from django.shortcuts import render
from courses.models import Course
from reports.models import Report
from lectures.models import Solution
from reports.serializers import (
    ReportCreateSerializer,
    ReportListSerializer,
    ReportDetailSerializer,
    CommentCreateSerializer,
)
from courses.permissions import (
    IsProfessorOrReadOnly,
    IsReportOwner,
)


class ReportsListView(generics.ListCreateAPIView):
    """Вывод списка отчётов и добавление отчёта преподавателем"""
    permission_classes = [IsProfessorOrReadOnly]

    def get_queryset(self):
        courses = Course.objects.filter(
            coursemember__user=self.request.user,
            coursemember__role="ST",
        )
        return Report.objects.filter(solution__task__lecture__course__in=courses, solution__status=Solution.COMPLETED)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReportCreateSerializer
        else:
            return ReportListSerializer

    def perform_create(self, serializer):
        solution = get_object_or_404(klass=Solution, id=serializer.validated_data["solution"])
        self.check_object_permissions(request=self.request, obj=solution)
        super().perform_create(serializer)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Вывод подробного отчёта"""
    permission_classes = [IsProfessorOrReadOnly]
    lookup_url_kwarg = 'report_id'

    def get_queryset(self):
        if self.request.method == "GET":
            courses = Course.objects.filter(
                coursemember__user=self.request.user,
                coursemember__role="ST",
            )
        else:
            courses = Course.objects.filter(
                coursemember__user=self.request.user,
                coursemember__role="PR",
            )
        return Report.objects.filter(solution__task__lecture__course__in=courses, solution__status=Solution.COMPLETED)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReportDetailSerializer
        else:
            return ReportCreateSerializer


class CommentCreateView(generics.CreateAPIView):
    """Добавление комментария"""
    permission_classes = [IsReportOwner]
    serializer_class = CommentCreateSerializer
