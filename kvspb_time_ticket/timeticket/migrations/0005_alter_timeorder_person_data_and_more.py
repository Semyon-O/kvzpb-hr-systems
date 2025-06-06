# Generated by Django 5.1.2 on 2025-04-14 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_alter_candidateaccess_status'),
        ('timeticket', '0004_rename_candidate_timeorder_person_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeorder',
            name='person_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time_order', to='candidate.candidate', verbose_name='Кандидат'),
        ),
        migrations.AlterField(
            model_name='timeorder',
            name='taken_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time_order', to='timeticket.timeuserwindow', verbose_name='Выбранное время'),
        ),
    ]
