# Generated by Django 5.1.3 on 2024-12-03 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorization', '0002_alter_customuser_is_superuser_delete_authcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
