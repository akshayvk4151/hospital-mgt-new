# Generated by Django 4.1.4 on 2023-03-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0003_doctors_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('phone', models.BigIntegerField(max_length=20)),
                ('remark', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'contact',
            },
        ),
    ]