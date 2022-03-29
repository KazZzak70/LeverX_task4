from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from lectures.service import opportunity_to_submit_solution
from lectures.serializers import (
    LectureCreateSerializer,
    LectureDetailSerializer,
    HometaskCreateSerializer,
    HometaskDetailSerializer,
    SolutionCreateSerializer,
    SolutionListSerializer,
)
from courses.permissions import (
    IsProfessorOrReadOnly,
    IsCourseMember,
)
from courses.models import Course, CourseMember
from lectures.service import SolutionFilter
from lectures.models import Lecture, Hometask, Solution


class LectureCreateView(generics.CreateAPIView):
    """Добавление лекции"""
    permission_classes = [IsProfessorOrReadOnly]
    serializer_class = LectureCreateSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(request=self.request, obj=serializer.validated_data["course"])
        super().perform_create(serializer)


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Вывод подробной информации о лекции, её изменение и удаление"""
    permission_classes = [IsProfessorOrReadOnly]
    lookup_url_kwarg = 'lecture_id'

    def get_queryset(self):
        return Lecture.objects.filter(course__members=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return LectureDetailSerializer
        return LectureCreateSerializer


class HometaskView(generics.ListCreateAPIView):
    """Вывод списка домашних заданий и добавление домашнего задания"""
    permission_classes = [IsProfessorOrReadOnly]

    def get_queryset(self):
        courses = Course.objects.filter(
            coursemember__user=self.request.user,
            coursemember__role="ST",
        )
        return Hometask.objects.filter(lecture__course__in=courses)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HometaskCreateSerializer
        return HometaskDetailSerializer

    def perform_create(self, serializer):
        self.check_object_permissions(request=self.request, obj=serializer.validated_data["lecture"])
        serializer.save()
        students = self.get_course_students(serializer.validated_data["lecture"])
        for student in students:
            Solution.objects.create(student=student, task=serializer.instance)

    def get_course_students(self, lecture: Lecture):
        course_students = CourseMember.objects.filter(course=lecture.course, role="ST")
        students_list = [student.user for student in course_students]
        return students_list


class SolutionListView(generics.ListCreateAPIView):
    """Вывод списка решений и добавление решения"""
    permission_classes = [IsCourseMember]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SolutionFilter

    def get_queryset(self):
        courses = Course.objects.filter(
            coursemember__user=self.request.user,
            coursemember__role="PR",
        )
        solutions = Solution.objects.filter(
            task__lecture__course__in=courses,
            status=Solution.COMPLETED,
        )
        return solutions

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SolutionCreateSerializer
        return SolutionListSerializer

    def create(self, request, *args, **kwargs):
        serializer = SolutionCreateSerializer(data=request.data)
        serializer.is_valid()
        solution = get_object_or_404(klass=Solution,
                                     student=self.request.user,
                                     task=serializer.validated_data["task"])
        self.check_object_permissions(request, solution.task)
        if opportunity_to_submit_solution(serializer.validated_data["task"].deadline_datetime):
            return Response(status=status.HTTP_403_FORBIDDEN)
        solution.solution = serializer.validated_data["solution"]
        solution.status = Solution.COMPLETED
        solution.save()
        return Response(status=status.HTTP_201_CREATED)
