# Generated by Django 3.2.3 on 2021-05-29 08:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210529_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publication_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
