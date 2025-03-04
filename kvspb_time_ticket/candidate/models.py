from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Почта")
    telegram_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.surname} {self.name} ({self.email})"

    class Meta:
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"


class CandidateAccess(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name="Кандидат")
    status = models.CharField(
        max_length=100,
        choices=(
            ('not_read', 'Не просмотрено'),
            ('access', "Документы приняты"),
            ("not_access", "Документы не были посланы")
        ),
        default='not_read',
        verbose_name="Статус документов"
    )

    def __str__(self):
        return f"{self.candidate} ({self.status})"

    class Meta:
        verbose_name = "Заявка кандидата"
        verbose_name_plural = "Заявки кандидатов"