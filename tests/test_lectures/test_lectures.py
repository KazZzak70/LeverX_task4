from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from faker import Faker
from model_bakery import baker

import pytest

from lectures.models import (
    Lecture,
    Hometask,
    Solution,
)


@pytest.mark.django_db
class TestLectureEndpoint:
    endpoint = "/api/v1/lectures/"
    faker = Faker()

    def test_lecture_create_valid(self, authorized_user, course, file):
        response_data = {
            "name": " ".join(self.faker.words(6)),
            "course": int(course.id),
            "presentation": SimpleUploadedFile(f"{self.faker.word()}.jpg", file),
        }
        response = authorized_user.post(self.endpoint, data=response_data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert Lecture.objects.filter(name=response_data["name"], course=course).exists()

    def test_lecture_retrieve_authorized(self, authorized_user, course, lecture):
        url = f"{self.endpoint}{lecture.id}/"
        response = authorized_user.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_lecture_retrieve_unauthorized(self, api_client, course, lecture):
        url = f"{self.endpoint}{lecture.id}/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_lecture_update_authorized_course_role_owner(self, authorized_user, lecture, file):
        url = f"{self.endpoint}{lecture.id}/"
        response_data = {
            "name": " ".join(self.faker.words(6)),
            "course": lecture.course.id,
            "presentation": SimpleUploadedFile(f"{self.faker.word()}.jpg", file),
        }
        response = authorized_user.put(url, data=response_data, format="multipart")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("name") == response_data.get("name")

    def test_lecture_update_authorized_course_role_student(self, student, lecture, file):
        url = f"{self.endpoint}{lecture.id}/"
        response_data = {
            "name": " ".join(self.faker.words(6)),
            "course": lecture.course.id,
            "presentation": SimpleUploadedFile(f"{self.faker.word()}.jpg", file),
        }
        response = student.put(url, data=response_data, format="multipart")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_lecture_delete_course_role_owner(self, authorized_user, lecture):
        url = f"{self.endpoint}{lecture.id}/"
        response = authorized_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Lecture.objects.filter(id=lecture.id).exists()

    def test_lecture_delete_course_role_student(self, student, lecture):
        url = f"{self.endpoint}{lecture.id}/"
        response = student.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestHometaskEndpoint:
    endpoint = "/api/v1/hometasks/"
    faker = Faker()

    def test_hometask_create_valid(self, authorized_user, lecture, test_user_student):
        response_data = {
            "name": " ".join(self.faker.words(6)),
            "task_description": self.faker.text(),
            "lecture": lecture.id,
        }
        response = authorized_user.post(self.endpoint, data=response_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Hometask.objects.filter(
            name=response_data.get("name"),
            task_description=response_data.get("task_description"),
            lecture=lecture.id,
        ).exists()
        task = Hometask.objects.get(
            name=response_data.get("name"),
            task_description=response_data.get("task_description"),
            lecture=lecture.id,
        )
        assert Solution.objects.filter(
            student=test_user_student.id,
            task=task,
        ).exists()

    def test_hometask_list_valid(self, student, hometask):
        response = student.get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 1


@pytest.mark.django_db
class TestSolutionEndpoint:
    endpoint = "/api/v1/solutions/"
    faker = Faker()

    def test_solution_create_valid(self, student, hometask, solution, test_user_student):
        response_data = {
            "task": hometask.id,
            "solution": self.faker.text(),
        }
        response = student.post(self.endpoint, data=response_data, format="json")
        solution = Solution.objects.get(
            student=test_user_student,
            task=hometask
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert solution.solution == response_data.get("solution")

    def test_solution_create_invalid_user_not_coursemember(self, authorized_user_not_coursemember, hometask):
        response_data = {
            "task": hometask.id,
            "solution": self.faker.text(),
        }
        response = authorized_user_not_coursemember.post(self.endpoint, data=response_data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_solution_list_valid(self, authorized_user, solution):
        response = authorized_user.get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 1
