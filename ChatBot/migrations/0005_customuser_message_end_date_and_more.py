# Generated by Django 4.2.6 on 2024-01-05 08:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ChatBot', '0004_customuser_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='message_end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='message_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
