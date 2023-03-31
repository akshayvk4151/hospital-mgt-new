# Generated by Django 4.1.4 on 2023-03-04 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=100)),
                ('dep_description', models.TextField()),
                ('dep_image', models.ImageField(upload_to='department/')),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=50)),
                ('patient_mobile', models.BigIntegerField()),
                ('patient_address', models.CharField(max_length=200)),
                ('patient_email', models.CharField(max_length=40)),
                ('patient_password', models.CharField(default='', max_length=10)),
                ('status', models.CharField(default='active', max_length=20)),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=50)),
                ('doctor_email', models.CharField(max_length=40)),
                ('doctor_phone', models.BigIntegerField()),
                ('doctor_address', models.CharField(max_length=200)),
                ('user_name', models.IntegerField(default=0)),
                ('password', models.CharField(default='', max_length=40)),
                ('doctor_gender', models.CharField(max_length=15)),
                ('doctor_image', models.ImageField(default='static/images/dummy-user.png', upload_to='doctor/')),
                ('doctor_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common_app.departments')),
            ],
            options={
                'db_table': 'doctors',
            },
        ),
    ]
