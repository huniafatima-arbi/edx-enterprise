# Generated by Django 3.2.12 on 2022-07-05 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0159_add_enable_learner_portal_offers'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisecustomer',
            name='enable_portal_learner_credit_management_screen',
            field=models.BooleanField(default=False, help_text='Specifies whether to allow access to the learner credit management screen in the admin portal.'),
        ),
        migrations.AddField(
            model_name='historicalenterprisecustomer',
            name='enable_portal_learner_credit_management_screen',
            field=models.BooleanField(default=False, help_text='Specifies whether to allow access to the learner credit management screen in the admin portal.'),
        ),
    ]
