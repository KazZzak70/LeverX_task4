from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """Курсы"""
    name = models.CharField(verbose_name="Название", max_length=150, unique=True)
    description = models.TextField(verbose_name="Описание")
    members = models.ManyToManyField(User, through='CourseMember')
    url = models.SlugField(verbose_name="Ссылка", max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CourseMember(models.Model):
    """Участники курса"""
    STUDENT = "ST"
    PROFESSOR = "PR"
    COURSE_ROLE_CHOICES = [
        (STUDENT, "Student"),
        (PROFESSOR, "Professor"),
    ]
    role = models.CharField(choices=COURSE_ROLE_CHOICES, default=STUDENT, max_length=2, verbose_name="Роль")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Участник курса"
        verbose_name_plural = "Участники курса"
