from django.contrib.auth.models import User
from django.db import models


class TimeUserWindow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата окна")
    time_start = models.TimeField(verbose_name="Время начала окна")
    time_end = models.TimeField(verbose_name="Время окончания окна")
    status = models.CharField(
        max_length=255, default="open", verbose_name="Зарезервировано кандидатом", choices={
        "close": "Запись закрыта",
        "open": "Запись открыта"
    },)

    def __str__(self):
        return f'{self.date} с {self.time_start} до {self.time_end}'


    class Meta:
        verbose_name = "Окно времени"
        verbose_name_plural = "Окна времени"


class TimeOrder(models.Model):
    person_data = models.CharField(max_length=255, verbose_name="ФИО кандидата")
    telegram_nickname = models.CharField(max_length=255, null=True, verbose_name="Имя в телеграмме")
    id_judgement_place = models.IntegerField(verbose_name="Номер судебного участка")
    taken_time = models.ForeignKey(TimeUserWindow, on_delete=models.SET_NULL, null=True, verbose_name="Выбранное время")

    def __str__(self):
        return f'{self.person_data} на {self.taken_time}'

    class Meta:
        verbose_name = "Зарезервированное окно"
        verbose_name_plural = "Зарезервированные окна"