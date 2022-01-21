import io
from PIL import Image
from faker import Faker
from model_bakery import baker
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from lectures.models import Lecture
from lectures.serializers import LectureDetailSerializer, LectureCreateSerializer


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

    def test_lecture_delete_course_role_student(self, student, lecture):
        url = f"{self.endpoint}{lecture.id}/"
        response = student.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
