from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from faker import Faker
import pytest

from courses.models import Course, CourseMember


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_data():
    return {'username': 'user1', 'password': 'qwerty921'}


@pytest.fixture
def test_user(user_data):
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def authorized_user(api_client, test_user):
    client = api_client
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def authorized_user_not_coursemember(api_client):
    client = api_client
    user = User.objects.create_user(username="user2", password="qwerty921")
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def course(test_user):
    course = baker.make(Course)
    CourseMember.objects.create(course=course, user=test_user, role=CourseMember.PROFESSOR)
    return course


@pytest.fixture
def student(api_client, course):
    client = api_client
    user = User.objects.create_user(username="user3", password="qwerty921")
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    CourseMember.objects.create(course=course, user=user, role=CourseMember.STUDENT)
    return client


@pytest.fixture
def course_data():
    faker = Faker()
    return {
        "name": " ".join(faker.words(5)),
        "description": faker.text(),
        "url": "_".join(faker.words(3)),
    }
