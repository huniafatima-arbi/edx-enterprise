# Generated by Django 3.2.23 on 2024-01-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0032_alter_historicalcanvasenterprisecustomerconfiguration_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvaslearnerassessmentdatatransmissionaudit',
            name='transmission_status',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='canvaslearnerdatatransmissionaudit',
            name='transmission_status',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]