from django.contrib.admin import TabularInline
from django.db import models

from judgment.models import Judgment

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    last_name = models.CharField(max_length=255, verbose_name="Отчество", null=True, blank=True)
    email = models.EmailField(verbose_name="Почта")
    telegram_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.surname} {self.name} ({self.email})"

    class Meta:
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"


class CandidateAccess(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="Кандидат", related_name='access')
    status = models.CharField(
        max_length=100,
        choices=(
            ('not_read', 'Не просмотрено'),
            ('access', "Документы приняты"),
            ("not_access", "Документы не были посланы"),
            ('give_enter', "Приглашение")
        ),
        default='not_read',
        verbose_name="Статус документов"
    )
    judgment_place = models.ForeignKey(to=Judgment, on_delete=models.SET_NULL, null=True, related_name='access')
    message_to_candidate = models.CharField(max_length=300, verbose_name='Сообщение кандидату', null=True, blank=True)

    def change_status_to_give_enter(self):
        self.status = "give_enter"
        self.save()

    def __str__(self):
        return f"{self.candidate} ({self.status})"

    class Meta:
        verbose_name = "Заявка кандидата"
        verbose_name_plural = "Заявки кандидатов"