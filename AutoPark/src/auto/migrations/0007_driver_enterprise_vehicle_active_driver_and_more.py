# Generated by Django 5.0.1 on 2024-02-08 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0006_driver_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='enterprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drivers', to='auto.enterprise'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='active_driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_vehicle', to='auto.driver'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='drivers',
            field=models.ManyToManyField(related_name='vehicles', to='auto.driver'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='enterprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='auto.enterprise'),
        ),
    ]