# Generated by Django 4.1.4 on 2023-03-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]