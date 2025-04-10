from django.contrib.auth.models import User
from django.db import models
from candidate import models as candidate_models

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
        permissions = (
            ('can_see_own_record', 'Может просматривать только свои записи'),
        )

class TimeOrder(models.Model):
    person_data = models.ForeignKey(candidate_models.Candidate, on_delete=models.CASCADE, verbose_name="Кандидат", null=True)
    taken_time = models.ForeignKey(TimeUserWindow, on_delete=models.SET_NULL, null=True, verbose_name="Выбранное время")

    def __str__(self):
        return f'{self.taken_time}'

    class Meta:
        verbose_name = "Зарезервированное окно"
        verbose_name_plural = "Зарезервированные окна"

    permissions = (
        ('can_see_own_record', 'Может просматривать только свои записи'),
    )