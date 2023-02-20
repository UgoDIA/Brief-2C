# Generated by Django 4.1.7 on 2023-02-20 06:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("classifr", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historique",
            name="date",
        ),
        migrations.AddField(
            model_name="historique",
            name="date_pred",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
