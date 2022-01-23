from rest_framework import status
from faker import Faker
from model_bakery import baker

import pytest

from reports.models import Mark, Report, Comment


@pytest.mark.django_db
class TestReportEndpoint:
    endpoint = "/api/v1/reports/"
    faker = Faker()

    def test_report_create_valid(self, authorized_user, solution, mark):
        response_data = {
            "solution": solution.id,
            "mark": mark.value,
        }
        response = authorized_user.post(self.endpoint, data=response_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == response_data

    def test_report_list_valid(self, student, report):
        response = student.get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 1

    def test_report_update_valid(self, authorized_user, solution, report):
        url = f"{self.endpoint}{report.id}/"
        mark = baker.make(Mark, value=10)
        response_data = {
            "solution": solution.id,
            "mark": mark.value
        }
        response = authorized_user.put(url, data=response_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_report_update_invalid(self, student, solution, report):
        url = f"{self.endpoint}{report.id}/"
        mark = baker.make(Mark, value=10)
        response_data = {
            "solution": solution.id,
            "mark": mark.value,
        }
        response = student.put(url, data=response_data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_report_retrieve_report_owner(self, student, report):
        url = f"{self.endpoint}{report.id}/"
        response = student.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("mark") == report.mark.value

    def test_report_retrieve_not_report_owner(self, authorized_user_not_coursemember, report):
        url = f"{self.endpoint}{report.id}/"
        response = authorized_user_not_coursemember.get(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_report_delete_valid(self, authorized_user, report):
        url = f"{self.endpoint}{report.id}/"
        response = authorized_user.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Report.objects.filter(
            id=report.id,
        ).exists()

    def test_report_delete_invalid(self, student, report):
        url = f"{self.endpoint}{report.id}/"
        response = student.delete(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCommentEndpoint:
    endpoint = "/api/v1/comments/"
    faker = Faker()

    def test_comment_create_course_role_student(self, student, report):
        response_data = {
            "report": report.id,
            "text": self.faker.text(),
            "role": Comment.STUDENT,
        }
        response = student.post(self.endpoint, data=response_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(
            report=response_data.get("report"),
            text=response_data.get("text"),
            role=response_data.get("role")
        ).exists()

    def test_comment_create_course_role_professor(self, authorized_user, report):
        response_data = {
            "report": report.id,
            "text": self.faker.text(),
            "role": Comment.PROFESSOR,
        }
        response = authorized_user.post(self.endpoint, data=response_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.filter(
            report=response_data.get("report"),
            text=response_data.get("text"),
            role=response_data.get("role")
        ).exists()
