from rest_framework import serializers
from lectures.serializers import SolutionInReportSerializer
from reports.models import (
    Report,
    Mark,
    Comment,
)


class ReportCreateSerializer(serializers.ModelSerializer):
    """Добавление отчёта"""
    mark = serializers.SlugRelatedField(slug_field="value", queryset=Mark.objects.all())

    class Meta:
        model = Report
        fields = ("solution", "mark", )


class ReportListSerializer(serializers.ModelSerializer):
    """Просмотр списка отчётов"""
    solution = serializers.SlugRelatedField(slug_field="solution", read_only=True)
    mark = serializers.SlugRelatedField(slug_field="value", read_only=True)

    class Meta:
        model = Report
        fields = ("id", "solution", "mark", )


class CommentCreateSerializer(serializers.ModelSerializer):
    """Добавление комментариев"""
    report = serializers.SlugRelatedField(slug_field="id", queryset=Report.objects.all())

    class Meta:
        model = Comment
        fields = ("text", "report", "role", )


class CommentsInReportSerializer(serializers.ModelSerializer):
    """Вывод комментариев в отчёте"""

    class Meta:
        model = Comment
        fields = ("role", "text", )


class ReportDetailSerializer(serializers.ModelSerializer):
    """Просмотр отчета"""
    mark = serializers.SlugRelatedField(slug_field="value", read_only=True)
    comments = CommentsInReportSerializer(many=True)
    solution = SolutionInReportSerializer()

    class Meta:
        model = Report
        fields = ("id", "mark", "solution", "comments", )
