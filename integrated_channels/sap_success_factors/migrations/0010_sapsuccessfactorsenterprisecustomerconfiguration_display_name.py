# Generated by Django 3.2.11 on 2022-01-31 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap_success_factors', '0009_auto_20220126_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='display_name',
            field=models.CharField(blank=True, default='', help_text='A configuration nickname.', max_length=30),
        ),
    ]
