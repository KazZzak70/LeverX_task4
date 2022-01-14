from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
import pytest

from courses.models import Course, CourseMember
from courses.serializers import (
    CourseDetailSerializer,
    CourseCreateSerializer,
    CourseMemberAddSerializer,
    CourseMemberDeleteSerializer,
)
from courses.models import (
    Course,
    CourseMember,
)


@pytest.mark.django_db
class TestRegistrationEndpoint:

    endpoint = "/api/v1/register/"

    def test_create_account(self, api_client, user_data):
        response = api_client.post(self.endpoint, data=user_data, format='json')
        assert response.status_code == 201
        assert response.data['username'] == user_data['username']


@pytest.mark.django_db
class TestLoginEndpoint:

    endpoint = "/api/v1/login/"

    def test_login_account(self, api_client, user_data, test_user):
        response = api_client.post(self.endpoint, data=user_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" and "refresh" in response.json()


@pytest.mark.django_db
class TestRefreshEndpoint:
    endpoint = "/api/v1/login/refresh/"

    def test_login_account(self, api_client, user_data, test_user):
        token = api_client.post("/api/v1/login/", data=user_data, format="json")
        refresh_token = token.json().get("refresh")
        response = api_client.post(self.endpoint, data={"refresh": refresh_token}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()


@pytest.mark.django_db
class TestCourseListViewEndpoint:
    endpoint = "/api/v1/courses/"

    def test_course_list_authorized(self, authorized_user, course):
        response = authorized_user.get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 1

    def test_course_list_unauthorized(self, api_client, course):
        response = api_client.get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_course_create_authorized(self, authorized_user, course_data, test_user):
        response = authorized_user.post(self.endpoint, data=course_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("name") == course_data["name"]
        assert CourseMember.objects.filter(
            course__name=course_data["name"],
            user=test_user,
            role=CourseMember.PROFESSOR
        ).exists()

    def test_course_create_unauthorized(self, api_client, course_data):
        response = api_client.post(self.endpoint, data=course_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCourseDetailViewEndpoint:
    endpoint = "/api/v1/courses/"

    def test_course_retrieve_authorized(self, authorized_user, course):
        url = f"{self.endpoint}{course.id}/"
        response = authorized_user.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_course_retrieve_unauthorized(self, api_client, course):
        url = f"{self.endpoint}{course.id}/"
        response = api_client.get(url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_course_update_authorized_course_role_owner(self, authorized_user, course):
        url = f"{self.endpoint}{course.id}/"
        new_course = baker.prepare(Course)
        course_dict = {
            "name": new_course.name,
            "description": new_course.description,
            "url": course.url,
        }
        serializer = CourseCreateSerializer(data=course_dict)
        if serializer.is_valid():
            course_dict = serializer.data
        response = authorized_user.put(url, data=course_dict, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serializer.data

    def test_course_update_authorized_course_role_student(self, course, student):
        url = f"{self.endpoint}{course.id}/"
        new_course = baker.prepare(Course)
        course_dict = {"name": new_course.name}
        serializer = CourseCreateSerializer(data=course_dict)
        if serializer.is_valid():
            course_dict = serializer.data
        response = student.put(url, data=course_dict, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_course_delete_course_role_owner(self, authorized_user, course):
        url = f"{self.endpoint}{course.id}/"
        response = authorized_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()

    def test_course_delete_course_role_student(self, student, course):
        url = f"{self.endpoint}{course.id}/"
        response = student.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCourseMemberEndpoint:
    endpoint = "/api/v1/coursemembers/"

    def test_add_coursemember_valid(self, authorized_user, course, test_user_not_coursemember):
        url = f"{self.endpoint}{course.id}/"
        response_dict = {
            "user": test_user_not_coursemember.username,
            "role": "ST",
        }
        serializer = CourseMemberAddSerializer(data=response_dict)
        if serializer.is_valid():
            response_dict = serializer.data
        response = authorized_user.post(url, data=response_dict, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_coursemember_invalid(self, student, course, test_user_not_coursemember):
        url = f"{self.endpoint}{course.id}/"
        response_dict = {
            "user": test_user_not_coursemember.username,
            "role": "ST",
        }
        serializer = CourseMemberAddSerializer(data=response_dict)
        if serializer.is_valid():
            response_dict = serializer.data
        response = student.post(url, data=response_dict, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_coursemember_valid(self, authorized_user, course, test_user_student):
        url = f"{self.endpoint}{course.id}/"
        response_dict = {"user": test_user_student.username}
        serializer = CourseMemberDeleteSerializer(data=response_dict)
        if serializer.is_valid():
            response_dict = serializer.data
        response = authorized_user.delete(url, data=response_dict, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_coursemember_invalid(self, test_user, course, student):
        url = f"{self.endpoint}{course.id}/"
        response_dict = {"user": test_user.username}
        serializer = CourseMemberDeleteSerializer(data=response_dict)
        if serializer.is_valid():
            response_dict = serializer.data
        response = student.delete(url, data=response_dict, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
