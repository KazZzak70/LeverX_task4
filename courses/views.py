from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    CourseCreateSerializer,
    CourseListSerializer,
    CourseDetailSerializer,
    CourseMemberAddSerializer,
    CourseMemberDeleteSerializer,
)
from courses.models import (
    Course,
    CourseMember,
)
from courses.permissions import (
    IsProfessorOrReadOnly,
    IsCourseMember,
    IsReportOwner,
)
from courses.functions import (
    add_user_to_course,
    delete_user_from_course,
)


class RegisterView(generics.CreateAPIView):
    """Регистрация"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CourseView(generics.ListCreateAPIView):
    """Вывод списка курсов и добавление курса"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CourseCreateSerializer
        else:
            return CourseListSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        add_user_to_course(user=self.request.user, course=serializer.instance, role=CourseMember.PROFESSOR)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Вывод подробной информации о курсе, его изменение и удаление"""
    permission_classes = [IsProfessorOrReadOnly]
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CourseDetailSerializer
        else:
            return CourseCreateSerializer


class CourseMemberView(APIView):
    """Добавление и удаление участников курса"""
    permission_classes = [IsProfessorOrReadOnly]

    def post(self, request, course_id):
        serializer = CourseMemberAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userobj = get_object_or_404(klass=User, username=serializer.validated_data["user"])

        course = get_object_or_404(klass=Course, id=course_id)
        self.check_object_permissions(request, course)

        add_user_to_course(user=userobj, course=course, role=serializer.validated_data["role"])

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, course_id):
        serializer = CourseMemberDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userobj = get_object_or_404(klass=User, username=serializer.validated_data["user"])

        course = get_object_or_404(klass=Course, id=course_id)
        self.check_object_permissions(request, course)

        if delete_user_from_course(user=userobj, course=course):
            return Response(status=status.HTTP_200_OK)
        Response(status=status.HTTP_403_FORBIDDEN)


