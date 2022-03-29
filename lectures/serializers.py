from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework import serializers
from lectures.models import (
    Lecture,
    Hometask,
    Solution,
)
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseInLectureSerializer(serializers.ModelSerializer):
    """Вывод курса в лекции"""
    class Meta:
        model = Course
        fields = ("id", "name", )


class LectureCreateSerializer(serializers.ModelSerializer):
    """Добавление лекции"""

    class Meta:
        model = Lecture
        fields = ("name", "course", "presentation", )


class LectureListSerializer(serializers.ModelSerializer):
    """Вывод списка лекций курса"""

    class Meta:
        model = Lecture
        fields = ("id", "name", )


class HometaskCreateSerializer(serializers.ModelSerializer):
    """Добавление домашнего задания"""

    class Meta:
        model = Hometask
        fields = ("name", "task_description", "lecture", "deadline_datetime", )

    def validate_deadline_datetime(self, value):
        if value <= now():
            raise serializers.ValidationError("Deadline can't be in the past")
        return value


class HometaskInLectureSerializer(serializers.ModelSerializer):
    """Вывод домашнего задания в лекции"""
    class Meta:
        model = Hometask
        fields = ("id", "name", "task_description", )


class LectureDetailSerializer(serializers.ModelSerializer):
    """Вывод лекции"""
    course = CourseInLectureSerializer()
    hometask = HometaskInLectureSerializer(many=True)

    class Meta:
        model = Lecture
        fields = ("id", "name", "course", "hometask", "presentation", )


class HometaskDetailSerializer(serializers.ModelSerializer):
    """Вывод домашнего задания"""
    lecture = LectureListSerializer()

    class Meta:
        model = Hometask
        fields = ("name", "task_description", "lecture", )


class SolutionCreateSerializer(serializers.ModelSerializer):
    """Добавление решения"""

    class Meta:
        model = Solution
        fields = ("task", "solution", )


class SolutionListSerializer(serializers.ModelSerializer):
    """Вывод списка решений"""
    task = HometaskInLectureSerializer()
    student = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Solution
        fields = ("student", "task", "solution", )


class SolutionInReportSerializer(serializers.ModelSerializer):
    """Просмотр решения в отчете"""
    task = HometaskInLectureSerializer()

    class Meta:
        model = Solution
        fields = ("task", "solution", )
