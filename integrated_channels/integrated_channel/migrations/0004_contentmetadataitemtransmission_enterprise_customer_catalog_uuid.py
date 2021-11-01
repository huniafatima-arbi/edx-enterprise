# Generated by Django 2.2.24 on 2021-09-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrated_channel', '0003_contentmetadataitemtransmission_content_last_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmetadataitemtransmission',
            name='enterprise_customer_catalog_uuid',
            field=models.UUIDField(blank=True, help_text='The enterprise catalog that this metadata item was derived from', null=True),
        ),
    ]