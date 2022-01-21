from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from faker import Faker
from PIL import Image
import io
import pytest

from courses.models import Course, CourseMember
from lectures.models import Lecture, Hometask


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_data():
    return {'username': 'user1', 'password': 'qwerty921'}


@pytest.fixture
def test_user(user_data):
    user = User.objects.create_user(**user_data)
    user.save()
    return user


@pytest.fixture
def test_user_not_coursemember():
    user = User.objects.create_user(username="user2", password="qwerty921")
    user.save()
    return user


@pytest.fixture
def authorized_user(api_client, test_user):
    client = api_client
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def authorized_user_not_coursemember(api_client, test_user_not_coursemember):
    client = api_client
    refresh = RefreshToken.for_user(test_user_not_coursemember)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def course(test_user):
    course = baker.make(Course)
    CourseMember.objects.create(course=course, user=test_user, role=CourseMember.PROFESSOR)
    return course


@pytest.fixture
def test_user_student(course):
    user = User.objects.create_user(username="user3", password="qwerty921")
    user.save()
    CourseMember.objects.create(course=course, user=user, role=CourseMember.STUDENT)
    return user


@pytest.fixture
def student(api_client, test_user_student):
    client = api_client
    refresh = RefreshToken.for_user(test_user_student)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def course_data():
    faker = Faker()
    return {
        "name": " ".join(faker.words(5)),
        "description": faker.text(),
        "url": "_".join(faker.words(3)),
    }


@pytest.fixture
def file():
    image = io.BytesIO()
    Image.new('RGB', (150, 150)).save(image, 'JPEG')
    image.seek(0)
    return image.getvalue()


@pytest.fixture
def lecture(course):
    lecture = baker.make(
        Lecture,
        course=course,
    )
    return lecture


@pytest.fixture
def hometask(lecture):
    hometask = baker.make(
        Hometask,
        lecture=lecture,
    )
    return hometask


@pytest.fixture
def file():
    image = io.BytesIO()
    Image.new('RGB', (150, 150)).save(image, 'JPEG')
    image.seek(0)
    return image.getvalue()


@pytest.fixture
def lecture(course):
    lecture = baker.make(
        Lecture,
        course=course,
    )
    return lecture


@pytest.fixture
def hometask(lecture):
    hometask = baker.make(
        Hometask,
        lecture=lecture,
    )
    return hometask
