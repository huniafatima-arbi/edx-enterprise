# Generated by Django 3.2.19 on 2024-02-20 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canvas', '0033_canvaslearnerdatatransmissionaudit_canvas_unique_enrollment_course_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalCanvasEnterpriseCustomerConfiguration',
        ),
    ]
