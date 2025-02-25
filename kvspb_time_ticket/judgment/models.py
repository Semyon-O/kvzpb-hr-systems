from django.contrib.auth.models import User
from django.db import models


class District(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True, verbose_name="Район")

    class Meta:
        verbose_name_plural = "Районы"

class Vacancy(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Должность")

    class Meta:
        verbose_name_plural = "Должности"

    def __str__(self):
        return f"{self.name}"

class Judgment(models.Model):
    id_judgment = models.IntegerField(primary_key=True, verbose_name='Номер участка')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Район")
    fio_judgment = models.CharField(max_length=255, verbose_name="ФИО судьи")
    phone = models.CharField(max_length=255, verbose_name="Телефон(ы) участка")
    description = models.TextField(null=True, blank=True, verbose_name="Описание участка")
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ответственный инспектор")
    vacancies = models.ManyToManyField(Vacancy, blank=True, through="VacancyInJudgment", verbose_name="Вакансии")

    def __str__(self):
        return f'Судебный участок №{self.id_judgment}'

    class Meta:
        verbose_name_plural = "Участки"
        verbose_name = "Участок"

class VacancyInJudgment(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name="Вакансия")
    judgment = models.ForeignKey(Judgment, on_delete=models.CASCADE, verbose_name="Участок")

    def __str__(self):
        return f"{self.judgment} - {self.vacancy}"

    class Meta:
        verbose_name_plural = "Вакансии в участке"
        verbose_name = "Вакансия в участке"