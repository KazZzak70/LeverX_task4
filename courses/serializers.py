from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from lectures.serializers import LectureListSerializer
from courses.models import (
    Course,
    CourseMember,
)


class RegisterSerializer(serializers.ModelSerializer):
    """Регистрация пользователя"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', )

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username")


class CourseCreateSerializer(serializers.ModelSerializer):
    """Добавление курса"""
    class Meta:
        model = Course
        fields = ("name", "description", "url", )


class CourseListSerializer(serializers.ModelSerializer):
    """Список курсов"""
    class Meta:
        model = Course
        fields = ("id", "name", )


class CourseMemberAddSerializer(serializers.ModelSerializer):
    """Добавление пользователя к курсу"""
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = CourseMember
        fields = ("role", "user", )

    def validate_role(self, value):
        if value.upper() not in [CourseMember.STUDENT, CourseMember.PROFESSOR]:
            raise serializers.ValidationError("Role must be 'ST' or 'PR' argument")
        return value


class CourseMemberDeleteSerializer(serializers.ModelSerializer):
    """Удаление студента из курса"""
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = CourseMember
        fields = ("user", )


class CourseDetailSerializer(serializers.ModelSerializer):
    """Полный курс"""
    lectures = LectureListSerializer(many=True)

    class Meta:
        model = Course
        fields = ("id", "lectures", "name", "description", "url", )
