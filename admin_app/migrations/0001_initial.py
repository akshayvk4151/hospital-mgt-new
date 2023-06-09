# Generated by Django 4.1.4 on 2023-03-28 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common_app', '0005_alter_contact_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('status', models.CharField(default='available', max_length=20)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common_app.doctors')),
            ],
            options={
                'db_table': 'consult',
            },
        ),
    ]
