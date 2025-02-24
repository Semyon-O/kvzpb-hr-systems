from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    telegram_id = models.CharField(max_length=255, blank=True, null=True)


class CandidateAccess(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=(
            ('not_read', 'Не просмотрено'),
            ('access', "Документы приняты"),
            ("not_access", "Документы не были посланы")
        ),
        default='not_read'
    )
