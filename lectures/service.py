from django.utils.timezone import now
from django_filters import rest_framework as filters
from lectures.models import Solution
from courses.models import CourseMember
from lectures.models import Hometask
from datetime import datetime


class SolutionFilter(filters.FilterSet):
    task = filters.BaseInFilter

    class Meta:
        model = Solution
        fields = ["task", ]


def opportunity_to_submit_solution(deadline_datetime: datetime):
    return now() > deadline_datetime


def get_course_student_emails(task_id: int):
    task = Hometask.objects.get(id=task_id)
    course_students = CourseMember.objects.filter(course=task.lecture.course, role=CourseMember.STUDENT)
    students_list = [(student.user.username, student.user.email) for student in course_students]
    return students_list
