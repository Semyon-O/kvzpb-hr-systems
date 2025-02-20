from django.contrib.auth.models import User
from django.db import models


class District(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)

class Vacancy(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Judgment(models.Model):
    id_judgment = models.IntegerField(primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    fio_judgment = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vacancies = models.ManyToManyField(Vacancy, blank=True, through="VacancyInJudgment")

    def __str__(self):
        return f'Судебный участок №{self.id_judgment}'

class VacancyInJudgment(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    judgment = models.ForeignKey(Judgment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.judgment} - {self.vacancy}"