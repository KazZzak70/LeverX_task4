from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from courses.models import (
    Course,
    CourseMember,
)


def add_user_to_course(user: User, course: Course, role: str):
    """Добавление пользователя к участникам курса"""
    coursemember = CourseMember.objects.create(user=user, course=course, role=role)
    coursemember.save()


def delete_user_from_course(user: User, course: Course):
    """Удаление пользователя из участников курса"""
    coursemember = get_object_or_404(klass=CourseMember, course=course, user=user)
    if coursemember.role == "PR":
        return False
    coursemember.delete()
    return True
