# Generated by Django 5.1.3 on 2024-12-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='AuthCode',
        ),
    ]
