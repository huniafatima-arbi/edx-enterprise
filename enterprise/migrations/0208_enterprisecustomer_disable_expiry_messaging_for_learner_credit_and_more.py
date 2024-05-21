# Generated by Django 4.2.13 on 2024-05-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0207_alter_enterprisegroupmembership_enterprise_customer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisecustomer',
            name='disable_expiry_messaging_for_learner_credit',
            field=models.BooleanField(default=False, help_text='If checked, learners and admins will not receive expiration-related email and other notifications regarding learner credit plans.', verbose_name='Disable expiration messaging for learner credit'),
        ),
        migrations.AddField(
            model_name='historicalenterprisecustomer',
            name='disable_expiry_messaging_for_learner_credit',
            field=models.BooleanField(default=False, help_text='If checked, learners and admins will not receive expiration-related email and other notifications regarding learner credit plans.', verbose_name='Disable expiration messaging for learner credit'),
        ),
    ]