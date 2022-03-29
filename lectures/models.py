from django.contrib.auth.models import User
from django.db import models
from courses.models import Course


class Lecture(models.Model):
    """Лекция"""
    name = models.CharField("Лекция", max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lectures")
    presentation = models.FileField(upload_to="presentations/", verbose_name="Презентация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"


class Hometask(models.Model):
    """Домашнее задание"""
    name = models.CharField("Задание", max_length=150)
    task_description = models.TextField("Описание задания")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, verbose_name="Лекция", related_name="hometask")
    start_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата/Время добавления")
    deadline_datetime = models.DateTimeField(verbose_name="Дедлайн", blank=True)
    average_mark = models.FloatField(verbose_name="Средняя отметка", blank=True, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class Solution(models.Model):
    """Решение домашнего задания"""
    INCOMPLETED = "undone"
    COMPLETED = "done"
    SOLUTION_STATUS_CHOICES = [
        (INCOMPLETED, "Incompleted"),
        (COMPLETED, "Completed"),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    task = models.ForeignKey(Hometask, on_delete=models.CASCADE, related_name="solution", verbose_name="Задание")
    solution = models.TextField(verbose_name="Решение", default="")
    status = models.CharField(choices=SOLUTION_STATUS_CHOICES, default=INCOMPLETED, max_length=6, verbose_name="Статус")

    def __str__(self):
        return f"{self.student} - {self.task} - {self.task.lecture.course}"

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"
