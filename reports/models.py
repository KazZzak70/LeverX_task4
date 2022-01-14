from django.db import models
from lectures.models import Solution


class Mark(models.Model):
    """Оценка"""
    value = models.PositiveSmallIntegerField(verbose_name="Значение", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"


class Report(models.Model):
    """Отчёт"""
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, verbose_name="Решение", related_name="report")
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name="Оценка")

    def __str__(self):
        return f"{self.mark} - {self.solution}"

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"


class Comment(models.Model):
    """Комментарий"""
    STUDENT = "ST"
    PROFESSOR = "PR"
    COURSE_ROLE_CHOICES = [
        (STUDENT, "Student"),
        (PROFESSOR, "Professor"),
    ]
    text = models.TextField(verbose_name="Текст", max_length=500)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="comments", verbose_name="Отчёт")
    role = models.CharField(choices=COURSE_ROLE_CHOICES, default=STUDENT, max_length=2, verbose_name="Роль")

    def __str__(self):
        return f"{self.role} - {self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
