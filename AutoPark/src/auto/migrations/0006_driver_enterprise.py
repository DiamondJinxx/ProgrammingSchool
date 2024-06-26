# Generated by Django 5.0.1 on 2024-02-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0005_vehicle_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('second_name', models.CharField(max_length=30)),
                ('patronymic', models.CharField(max_length=40)),
                ('salary', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Водитель',
                'verbose_name_plural': 'Водители',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('city', models.CharField(max_length=3)),
                ('foundation_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
            },
        ),
    ]
