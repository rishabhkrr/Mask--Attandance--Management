# Generated by Django 3.2.2 on 2021-05-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_base', '0002_alter_attendancetable_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetable',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]